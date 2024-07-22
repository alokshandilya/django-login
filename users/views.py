from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm, BlogPostForm
from .models import BlogPost, CustomUser, Appointment
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
from django.http import HttpResponseBadRequest


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


@login_required
def create_blog_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect("dashboard")
    else:
        form = BlogPostForm()
    return render(request, "create_blog_post.html", {"form": form})


@login_required
def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, "blog_detail.html", {"post": post})


@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, is_doctor=True)

    if request.method == "POST":
        required_speciality = request.POST.get("required_speciality")
        appointment_date = request.POST.get("appointment_date")
        appointment_start_time = request.POST.get("appointment_start_time")

        # Parse date and time
        try:
            appointment_start = datetime.strptime(f"{appointment_date} {appointment_start_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return HttpResponseBadRequest("Invalid date or time format")

        appointment_end = appointment_start + timedelta(minutes=45)

        # Create the appointment
        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            speciality=required_speciality,
            start_time=appointment_start,
            end_time=appointment_end
        )

        return render(request, "appointment_confirmation.html", {
            "doctor": doctor,
            "appointment_date": appointment_start.date(),
            "appointment_start_time": appointment_start.time(),
            "appointment_end_time": appointment_end.time()
        })

    return render(request, "book_appointment.html", {"doctor": doctor})


@login_required
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctor = appointment.doctor
    speciality = appointment.speciality
    date = appointment.start_time.strftime('%Y-%m-%d')
    start_time = appointment.start_time.strftime('%H:%M')
    end_time = appointment.end_time.strftime('%H:%M')

    return render(request, "appointment_details.html", {
        "doctor": doctor,
        "speciality": speciality,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
    })


@login_required
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_patient:
            doctors = CustomUser.objects.filter(is_doctor=True)
            blog_posts = BlogPost.objects.filter(draft=False)
            appointments = Appointment.objects.filter(patient=request.user)
            return render(
                request,
                "patient_dashboard.html",
                {
                    "doctors": doctors,
                    "blog_posts": blog_posts,
                    "appointments": appointments,
                },
            )
        elif request.user.is_doctor:
            blog_posts = BlogPost.objects.filter(author=request.user)
            return render(request, "doctor_dashboard.html", {"blog_posts": blog_posts})
    return redirect("login")


@login_required
def view_blog_posts(request):
    if request.user.is_patient:
        blog_posts = BlogPost.objects.filter(draft=False)
    elif request.user.is_doctor:
        blog_posts = BlogPost.objects.filter(author=request.user)
    else:
        return redirect("login")

    return render(request, "view_blog_posts.html", {"blog_posts": blog_posts})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = BlogPostForm(instance=post)

    return render(request, "edit_post.html", {"form": form, "post": post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == "POST":
        post.delete()
        return redirect("dashboard")

    return render(request, "delete_post.html", {"post": post})


@login_required
def view_blog_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    return render(request, "view_blog_post.html", {"blog_post": blog_post})
