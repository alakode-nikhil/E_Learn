from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from manager.models import Course, Chapter, ChapterCompleted, ChapterRating 
from .models import IsPurchased, CanRate, CanRateChapter, FeedBack
from trainer.models import Rating, Contact
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from django.urls import reverse
from moviepy.editor import VideoFileClip
import os

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

@login_required
def goto_course(request, course_id):

    course = Course.objects.get(id = course_id)
    chapters = course.chapter_set.all()
    current = chapters.first()
    chapter_completed = ChapterCompleted.objects.get(chapter = current, student = request.user)
    possible,_ = CanRate.objects.get_or_create(course = course, student = request.user)
    pos_chapter,_ = CanRateChapter.objects.get_or_create(chapter = current, student = request.user)

    if chapter_completed and not chapter_completed.completed:
        chapter_completed.completed = True
        chapter_completed.save()
    total_time = 0
    completed_time = 0
    for chp in chapters:
        video_path = os.path.join(settings.MEDIA_ROOT, str(chp.chapter_video))
        chp_completed = ChapterCompleted.objects.get(chapter = chp, student = request.user)
        clip = VideoFileClip(video_path)
        duration = clip.duration
        total_time += duration
        if chp_completed and chp_completed.completed:
            completed_time += duration

    try:
        progress_percentage = int((completed_time/total_time) * 100)
       
    except ZeroDivisionError:
        return render(request, 'error/zero_division.html')

    return render(request, 'student/goto_course.html', {'course':course, 'chapters':chapters, 'current':current, 'possible':possible, 'progress':progress_percentage, 'pos_chapter':pos_chapter})

@login_required
def goto_chapter(request, chapter_id):

    chapter = Chapter.objects.get(id = chapter_id)
    course = chapter.course
    chapters = course.chapter_set.all()
    chapter_completed = ChapterCompleted.objects.get(chapter = chapter, student = request.user)
    possible,_ = CanRate.objects.get_or_create(course = course, student = request.user)
    pos_chapter,_ = CanRateChapter.objects.get_or_create(chapter = chapter, student = request.user)
    if chapter_completed and not chapter_completed.completed:
        chapter_completed.completed = True
        chapter_completed.save()
    total_time = 0
    completed_time = 0
    for chp in chapters:
        video_path = os.path.join(settings.MEDIA_ROOT, str(chp.chapter_video))
        clip = VideoFileClip(video_path)
        chp_completed = ChapterCompleted.objects.get(chapter = chp, student = request.user)
        duration = clip.duration
        total_time += duration
        if chp_completed and chp_completed.completed:
            completed_time += duration
    try:
        progress_percentage = int((completed_time/total_time) * 100)
        
    except ZeroDivisionError:
        return render(request, 'error/zero_division.html')
    
    return render(request, 'student/goto_course.html', {'course':course, 'chapters':chapters, 'current':chapter, 'possible':possible, 'pos_chapter':pos_chapter, 'progress':progress_percentage,})

@login_required
def check_trainer(request, trainer_id):

    trainer = User.objects.get(id=trainer_id)
    trainer_rating, created = Rating.objects.get_or_create(user = trainer)

    if created:
        trainer_rating.user = trainer
        trainer_rating.score = 0
        trainer_rating.count = 0
        trainer_rating.save()

    return render(request, 'student/check_trainer.html',{'trainer_rating': trainer_rating})

@login_required
def rate_trainer(request, trainer_id):
    trainer = User.objects.get(id = trainer_id)
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id = course_id)

    if request.method == 'POST':
        rating = int(request.POST.get('rating_input'))
    
        student = request.user
        progress = CanRate.objects.get(course = course, student = student)
        progress.can_rate = False
        progress.save()

        trainer_rating,created = Rating.objects.get_or_create(user = trainer)
        if created or trainer_rating.count == 0:
            trainer_rating.score += rating
            trainer_rating.count += 1
        
        else:
            trainer_rating.score = int(((trainer_rating.score * trainer_rating.count) + rating)/(trainer_rating.count + 1))
            trainer_rating.count += 1

        trainer_rating.save()

        return redirect('rate_success')
        
    return render(request, 'student/rate_trainer.html',{'course':course})


@login_required
def success_rating(request):
    return render(request, 'student/success_rating.html')

@login_required
def trainer_details(request, trainer_id):
    trainer = User.objects.get(id = trainer_id)
    contact_det,_ = Contact.objects.get_or_create(user = trainer)
    rating,_ = Rating.objects.get_or_create(user = trainer)
    print(rating.score)


    return render(request, 'student/trainer_details.html', {'contact':contact_det, 'rating':rating, 'trainer':trainer})

class StudentDetails(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'student/student_detail.html'
    context_object_name = 'student'

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)
    
@login_required
def rate_chapter(request, chapter_id):
    
    chapter = Chapter.objects.get(id = chapter_id)
    if request.method == 'POST':

        pos_chapter,_ = CanRateChapter.objects.get_or_create(chapter =chapter, student = request.user)
        rating = int(request.POST.get('rating_input')) if request.POST.get('rating_input') else  1
        pos_chapter.can_rate = False
        pos_chapter.save()

        ch_rating,created = ChapterRating.objects.get_or_create(chapter = chapter)
        if created or ch_rating.count == 0:
            ch_rating.chapter_rating += rating
            ch_rating.count += 1
        
        else:
            ch_rating.chapter_rating = int(((ch_rating.chapter_rating * ch_rating.count) + rating)/(ch_rating.count + 1))
            ch_rating.count += 1

        ch_rating.save()

        return redirect('success_rate_chapter', chapter_id)

    return render(request, 'student/rate_chapter.html', {'chapter':chapter})

@login_required
def success_chapter_rating(request, chapter_id):
    id = chapter_id
    return render(request, 'student/success_rate_chapter.html', {'id':id})

@login_required    
def update_feedback(request,pk):

    student = request.user
    course = Course.objects.get(id = pk)
    feedback,_ = FeedBack.objects.get_or_create(student = student, course = course)

    if request.method == 'POST':

        content = request.POST.get('feedback')
        feedback.content = content
        feedback.save()

        return redirect('student_home')
    
    return render(request, 'student/update_feedback.html', {'feedback':feedback})

