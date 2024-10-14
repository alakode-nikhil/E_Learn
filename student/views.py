from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from manager.models import Course
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeView(LoginRequiredMixin, ListView):

    model = Course
    template_name = 'student/home.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Course.objects.filter(ispurchased__is_purchased = True, ispurchased__student = self.request.user)
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)
    
class CourseView(LoginRequiredMixin, ListView):

    model = Course
    template_name = 'student/courses.html'
    context_object_name = 'courses'
    paginate_by = 10

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)
    
class CourseTrainer(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'student/course_trainer.html'
    context_object_name = 'course'

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)