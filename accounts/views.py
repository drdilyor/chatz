from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'registration/signup.html', context={
            'form': UserCreationForm()
        })
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    return redirect('signup')
