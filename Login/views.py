from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
@login_required
def home(request):
    return render(request, 'home.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        else:
            User.objects.create_user(username=username, password=password1, email=email)
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    
    return render(request, 'register.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')




@login_required
def change_password(request):
    if request.method == "POST":
        pc = PasswordChangeForm(user=request.user, data=request.POST)
        if pc.is_valid():
            pc.save()
            update_session_auth_hash(request, pc.user)  
            return redirect('home')
    else:
        pc = PasswordChangeForm(user=request.user) 

    return render(request, 'changepassword.html', {'pc': pc})
