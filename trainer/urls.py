from django.urls import path
from . import views

urlpatterns =[
    path('', views.HomeView.as_view(), name='trainer_home'),
    path('student_details/<int:course_id>/', views.StudentList.as_view(), name='course_student_list')
]