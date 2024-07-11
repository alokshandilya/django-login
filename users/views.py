from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


def dashboard(request):
    if request.user.is_patient:
        return render(request, "patient_dashboard.html")
    elif request.user.is_doctor:
        return render(request, "doctor_dashboard.html")
    else:
        return redirect("login")
