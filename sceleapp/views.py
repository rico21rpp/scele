from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect

from sceleapp.forms import RegisterForm

from sceleapp.models import Gamification

# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    is_gamified = Gamification.objects.first().is_gamified
    print("is_gamified", is_gamified)
    return render(request, 'dashboard.html', {'logged_in': True, 'user_fullname': user.get_full_name(), 'is_gamified': is_gamified})

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                usname = form.cleaned_data.get('username')
                psword = form.cleaned_data.get('password')
                user = authenticate(username=usname, password=psword)
                if user is not None:
                    auth_login(request, user)
                    messages.info(request, f"You are logged in as {usname}")
                    return redirect("dashboard") # url link
                else:
                    messages.error(request, "Invalid usernameor password")
            else:
                messages.error(request, "Invalid usernameor password")
        else:
            form = AuthenticationForm()
        return render(request, 'auth/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

# sourcecode: https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                # uname = form.cleaned_data.get('username')
                # raw_password = form.cleaned_data.get('password1')
                return redirect('login')
        else:
            form = RegisterForm()
        return render(request, 'auth/register.html', {'form': form})