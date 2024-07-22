from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create_blog_post/", views.create_blog_post, name="create_blog_post"),
    path("view_blog_posts/", views.view_blog_posts, name="view_blog_posts"),
    path("blog_detail/<int:post_id>/", views.blog_detail, name="blog_detail"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("view_blog_post/<int:post_id>/", views.view_blog_post, name="view_blog_post"),
    path("book_appointment/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path("appointment_details/<int:appointment_id>/", views.appointment_details, name="appointment_details"),
    path('oauth2callback/', views.google_oauth2_callback, name='google_oauth2_callback'),
]
