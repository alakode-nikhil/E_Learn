from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='student_home'),
    path('purchase_course/', views.CourseView.as_view(), name='purchase_courses'),
    path('check_trainer/<trainer_id>/', views.check_trainer, name='check_trainer'),
    path('purchase_course/<course_id>/', views.purchase_course, name = 'purchase_course'),
    path('purchase_success/<pk>/', views.success, name='success'),
    path('purchase_cancel/', views.cancel, name='cancel'),
    path('already_purchased/<pk>', views.already_purchased, name='already_purchased'),
    path('course/<course_id>/', views.goto_course, name = 'goto_course'),
    path('chapter/<chapter_id>/', views.goto_chapter, name = 'goto_chapter'),
    path('rate_trainer/<trainer_id>/', views.rate_trainer, name = 'rate_trainer'),
    path('rate_success/', views.success_rating, name='rate_success'),
    path('trainer_details/<trainer_id>/', views.trainer_details, name='trainer_details'),
    path('student_details/<int:pk>/', views.StudentDetails.as_view(), name='student_details'),
    path('chapter_rating/<chapter_id>/', views.rate_chapter, name = 'rate_chapter'),
    path('rate_chapter_success/<chapter_id>/', views.success_chapter_rating, name='success_rate_chapter'),
    path('update_feedback/<pk>/', views.update_feedback, name='update_feedback'),

]