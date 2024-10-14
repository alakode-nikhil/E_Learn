from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from manager.models import Course, Chapter, ChapterCompleted
from .models import IsPurchased
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from django.urls import reverse

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

@login_required    
def purchase_course(request, course_id):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    course = Course.objects.get(id= course_id)

    already_purchased = IsPurchased.objects.get(student = request.user, course = course)
    if already_purchased:
        return redirect('already_purchased', pk = course.id)

    if request.method == 'POST':

        line_items = []
        if course:
            line_item ={
                'price_data':{
                    'currency': 'INR',
                    'unit_amount':int(course.price * 100),
                    'product_data':{
                        'name':course.course_name
                    },
                },
                'quantity':1
            }
        line_items.append(line_item)

        if line_items:

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success',kwargs={'pk':course_id})),
                cancel_url=request.build_absolute_uri(reverse('cancel')),
            )

            return redirect(checkout_session.url,code=303)
    
@login_required
def success(request, pk):
    course = Course.objects.get(id=pk)
    student = request.user
    bought = IsPurchased.objects.create(student = student, course = course, is_purchased = True)
    chapters = course.chapter_set.all()
    for chapter in chapters:
        progress = ChapterCompleted.objects.create(chapter = chapter, student = student, completed = False)
        progress.save()

    bought.save()

    return render(request, 'student/success.html')

@login_required
def cancel(request):
    return render(request, 'student/cancel.html')

@login_required
def already_purchased(request, pk):
    course = Course.objects.get(id=pk)

    return render(request, 'student/already_purchased.html',{'course':course})

