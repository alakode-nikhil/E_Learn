from django.urls import path
from . import views

urlpatterns =[
    path('', views.TestView.as_view(), name='trainer_home')
]