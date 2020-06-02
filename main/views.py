from django.shortcuts import render
from django.http import HttpResponse
from .models import Tutorial
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from .forms import NewUserForm


# Create your views here.


def homepage(request):
    return render(request=request,
                  template_name='main/home.html',
                  context={"tutorials": Tutorial.objects.all})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})

def logout_request(request):
    logout(request)
    return redirect("main:homepage")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    form = AuthenticationForm()
    return render(request = request,
                  template_name = "main/login.html",
                  context={"form":form})
