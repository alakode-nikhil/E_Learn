from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(), name='manager_home'),
    path('student_list/',views.ListStudent.as_view(), name='list_students'),
    path('trainer/list', views.ListTrainer.as_view(), name='list_trainers'),
    path('update_user/<pk>', views.update_user, name='update_user'),
    path('delete/<pk>', views.DeleteUser.as_view(), name='delete_user'),
    path('add_course/', views.CreateCourse.as_view(), name='create_course'),
    path('add_chapter/<course_id>', views.add_chapter, name='add_chapter'),
    path('course_details/<course_id>', views.course_details, name='course_details')
]