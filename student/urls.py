from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='student_home'),
    path('purchase_course/', views.CourseView.as_view(), name='purchase_courses'),
    path('course_trainer/<int:pk>', views.CourseTrainer.as_view(), name='course_trainer'),
]