from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, "home.html",{})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return HttpResponse('Please fill in all fields', status=400)
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User is valid, log them in
            login(request, user)
            # Redirect to the home page
            return redirect(reverse('home'))
        else:
            # Invalid username or password
            return HttpResponse('Invalid username or password', status=400)
    
    return render(request, 'login.html')