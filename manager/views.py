from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeView(LoginRequiredMixin, ListView):

    model= Course
    template_name = 'manager/home.html'
    context_object_name = 'courses'
    paginate_by = 10

    def handle_no_permission(self) -> HttpResponseRedirect:
        return render(self.request, 'error/denied_access.html', status=403)