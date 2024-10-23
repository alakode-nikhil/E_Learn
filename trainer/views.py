from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from manager.models import Course, ChapterCompleted, Chapter
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from moviepy.editor import VideoFileClip


# Create your views here.

class HomeView(LoginRequiredMixin, ListView):

    model = Course
    template_name = 'trainer/home.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Course.objects.filter(trainer = self.request.user)
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)
    
class StudentList(LoginRequiredMixin, ListView):

    model = User
    template_name = 'trainer/student_list.html'
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

    return render(request, 'trainer/student_progress.html', {'course':course, 'student':student, 'progress':progress_percentage})

@login_required
def add_chapter(request, course_id):

    course = Course.objects.get(id = course_id)

    if request.method == 'POST':
        chapter_name = request.POST.get('chapter_name')
        chapter_video = request.FILES.get('chapter_video')

        chapter= Chapter.objects.create(chapter_name = chapter_name, chapter_video = chapter_video, course = course)
        chapter.save()
        return redirect('trainer_home')

    return render(request, 'trainer/add_chapter.html',{'course':course})