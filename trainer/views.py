from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from manager.models import Course
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


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
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)