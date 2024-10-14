from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def register_user(request):

    user_type = request.GET.get('type')

    if request.method =='POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        if user_type == 'MANAGER':
            is_superuser = True
        else:
            is_superuser = False
        password = request.POST.get('pass')
        cpass = request.POST.get('cpass')

        if cpass != password:
            messages.info(request,'Password mismatch')
            return redirect('register')
        
        if User.objects.filter(username = username).exists():
            messages.info(request,'Username already exists')
            return redirect('register')
        if User.objects.filter(email = email).exists():
            messages.info(request,'Email already exists')
            return redirect('register')
        user = User.objects.create_user(username=username, first_name= first_name, last_name = last_name, is_superuser = is_superuser, password= password, email=email)
        user.save()
        profile = Profile.objects.create(user = user, type = user_type, user_id = user.id)
        profile.save()
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('manager_home')
        return redirect('login')
    
    return render(request, 'profiles/register.html')

def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(username=username, password= password)
        try:
            if user is not None:
                profle = user.profile
                user_type = profle.type
                login(request,user)
                if user_type == 'STUDENT':
                    return redirect('student_home')
                elif user_type == 'TRAINER':
                    return redirect('trainer_home')
                elif user_type == 'MANAGER':
                    return redirect('manager_home')
                else:
                    messages.info(request,'Random Type')
                    return redirect('login')
            else:
                messages.info(request,'Invalid Credentials')
                return redirect('login')
        except:
            messages.error(request,'Invalid Role')
    
    return render(request,'profiles/login.html')

def logout_user(request):

    logout(request)
    return redirect('login')
