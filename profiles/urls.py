from django.urls import path
from . import views

urlpatterns =[
    path('register/',views.register_user, name='register'),
    path('', views.login_user, name='login'),
    path('', views.logout_user, name='logout')
]