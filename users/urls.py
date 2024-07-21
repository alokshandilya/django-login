from django.urls import path
from .views import (
    signup,
    dashboard,
    create_blog_post,
    view_blog_posts,
    blog_detail,
    edit_post,
    delete_post,
    view_blog_post,
    book_appointment,
)

urlpatterns = [
    path("", signup, name="signup"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create_blog_post/", create_blog_post, name="create_blog_post"),
    path("view_blog_posts/", view_blog_posts, name="view_blog_posts"),
    path("blog_detail/<int:post_id>/", blog_detail, name="blog_detail"),
    path("edit_post/<int:post_id>/", edit_post, name="edit_post"),
    path("delete_post/<int:post_id>/", delete_post, name="delete_post"),
    path("view_blog_post/<int:post_id>/", view_blog_post, name="view_blog_post"),
    path("book_appointment/<int:doctor_id>/", book_appointment, name="book_appointment"),
]
