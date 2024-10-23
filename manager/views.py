from typing import Any
from django.db.models.query import QuerySet, Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from .models import Course, Chapter, ChapterCompleted
from student.models import FeedBack, PaymentDetails
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .form import CourseForm
import os
from django.conf import settings
from moviepy.editor import VideoFileClip

# Create your views here.

class HomeView(LoginRequiredMixin, ListView):

    model= Course
    template_name = 'manager/home.html'
    context_object_name = 'courses'
    paginate_by = 10

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)
    
class ListStudent(LoginRequiredMixin, ListView):

    model = User

    template_name = 'manager/list_users.html'

    context_object_name = 'users'

    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return User.objects.filter(profile__type = 'STUDENT')
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)
    
class ListTrainer(LoginRequiredMixin, ListView):

    model = User

    template_name = 'manager/list_users.html'

    context_object_name = 'users'

    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return User.objects.filter(profile__type = 'TRAINER')
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)

@login_required    
def update_user(request,pk):

    user = User.objects.get(pk=pk)

    if request.method == 'POST':

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        
        if User.objects.exclude(pk=pk).filter(username = username).exists():
            messages.info(request,'Username already exists')
            return redirect(reverse('update_user',kwargs={'pk':user.pk}))
        if User.objects.exclude(pk=pk).filter(email = email).exists():
            messages.info(request,'Email already exists')
            return redirect(reverse('update_user',kwargs={'pk':user.pk}))
        user.username = username
        user.first_name = first_name
        user.last_name  = last_name
        user.email = email
        user.profile.type = user_type
        print(user.profile.type)
        user.save()
        user.profile.save()
        return redirect('manager_home')
    
    return render(request, 'manager/update_user.html',{'user':user})

class DeleteUser(LoginRequiredMixin, DeleteView):

    model = User
    template_name = 'manager/delete_user.html'
    success_url = reverse_lazy('manager_home')

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)

class CreateCourse(LoginRequiredMixin, CreateView):

    model = Course
    form_class = CourseForm

    template_name = 'manager/create_course.html'

    success_url = reverse_lazy('manager_home')

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)

@login_required
def add_chapter(request, course_id):

    course = Course.objects.get(id = course_id)

    if request.method == 'POST':
        chapter_name = request.POST.get('chapter_name')
        chapter_video = request.FILES.get('chapter_video')

        chapter= Chapter.objects.create(chapter_name = chapter_name, chapter_video = chapter_video, course = course)
        chapter.save()
        return redirect('manager_home')

    return render(request, 'manager/add_chapter.html')


@login_required
def course_details(request, course_id):

    course = Course.objects.get(id = course_id)
    chapters = course.chapter_set.all()
    current = chapters.first()

    return render(request, 'manager/course_details.html', {'course':course, 'chapters':chapters, 'current':current})

class DeleteCourse(LoginRequiredMixin, DeleteView):

    model = Course
    template_name = 'manager/delete_course.html'
    success_url = reverse_lazy('manager_home')

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)
    
class SearchCourse(LoginRequiredMixin, ListView):

    model = Course
    template_name = 'manager/search_course.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')

        return Course.objects.filter(
            Q(course_name__icontains = query)
        )
    
class StudentList(LoginRequiredMixin, ListView):

    model = User
    template_name = 'manager/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id = course_id)
        return User.objects.filter(profile__type = 'STUDENT', ispurchased__course = course, ispurchased__is_purchased = True)
    
    def get_context_data(self, **kwargs):
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id = course_id)
        context = super().get_context_data(**kwargs)
        context['course'] = course
        return context
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)
    
@login_required
def student_progress(request, course_id, student_id):

    course = Course.objects.get(id = course_id)
    chapters = course.chapter_set.all()
    student = User.objects.get(id= student_id)

    total_time = 0
    completed_time = 0
    for chapter in chapters:
        chapter_completed,_ = ChapterCompleted.objects.get_or_create(chapter = chapter, student = student)
        video_path = os.path.join(settings.MEDIA_ROOT, str(chapter.chapter_video))
        clip = VideoFileClip(video_path)
        duration = clip.duration
        total_time += duration
        if chapter_completed and chapter_completed.completed:
            completed_time += duration

    try:
        progress_percentage = int((completed_time/total_time) * 100)
       
    except ZeroDivisionError:
        return render(request, 'error/zero_division.html')
    
    print(progress_percentage)

    return render(request, 'manager/student_progress.html', {'course':course, 'student':student, 'progress':progress_percentage})

@login_required
def student_feedback(request, course_id, student_id):

    student = User.objects.get(id = student_id)
    course = Course.objects.get(id = course_id)
    feedback,_ = FeedBack.objects.get_or_create(student = student, course = course)

    return render(request, 'manager/student_feedback.html', {'feedback':feedback})

@login_required
def update_payment_details(request, course_id, student_id):
    course = Course.objects.get(id = course_id)
    student = User.objects.get(id = student_id)

    pay_details,_ = PaymentDetails.objects.get_or_create(course= course, student = student)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        payment_date = request.POST.get('payment_date')
        payment_amount = request.POST.get('payment_amount')

        pay_details.payment_method = payment_method
        pay_details.payment_date = payment_date
        pay_details.payment_amount = payment_amount
        pay_details.save()

        return redirect('mng_course_student_list',course_id = course.id)
    
    return render(request,'manager/update_payment.html', {'pay_details':pay_details})
