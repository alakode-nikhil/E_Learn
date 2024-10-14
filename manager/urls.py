from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(), name='manager_home'),
    path('student_list/',views.ListStudent.as_view(), name='list_students'),
    path('trainer/list', views.ListTrainer.as_view(), name='list_trainers'),
    path('update_user/<pk>', views.update_user, name='update_user'),
    path('delete/<pk>', views.DeleteUser.as_view(), name='delete_user'),
]