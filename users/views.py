from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# ============================================================
# AUTHENTICATION VIEWS
# ============================================================

# register/
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        # Register the user using Django's built-in User model
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists. Please choose another.'})
        if password1 != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match. Please try again.'})
        User.objects.create_user(username=username, password=password1)

        user = authenticate(request, username=username, password=password1)
        # Redirect to dashboard
        login(request, user)
        return HttpResponseRedirect('/dashboard')

# login/
def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard')
        return render(request, 'login.html')
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/dashboard')
        else:
            return render(request, 'login.html', {'error': 'Incorrect username or password. Please try again.'})

# logout/
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return render(request, 'login.html', {'message': 'You have been logged out successfully.'})
    else:
        return HttpResponseRedirect('/dashboard')