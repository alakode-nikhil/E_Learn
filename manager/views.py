from typing import Any
from django.db.models.query import QuerySet, Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView
from .models import Course, Chapter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .form import CourseForm

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