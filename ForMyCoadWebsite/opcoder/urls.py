from django.urls import path
from django.contrib.auth.views import LoginView
from .import views, views1, views2

urlpatterns = [
    # For views
    path('', views.index, name='opcoder'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('blogs/', views.blog, name='blog'),
    path('blogpost/<str:slug>',views.blogpost,name='blogpost'),
    path('like_blog_post/<int:pk>/', views.like_blog_post, name='like_blog_post'),
    path('blog_comment/<int:pk>/', views.add_comment, name='blog_comment'),

    # For views1
    path('feedback/', views1.feedback, name='feedback'),
    path('login/', views1.login_page, name='login_page'),
    path('logout/', views1.logout_page, name='logout'),
    path('register/', views1.register, name='register'),
    path('change_password/', views1.change_password, name='change_password'),
    path('error404/', views1.error_page, name='error404'),

    # For views2
    path('videos/', views2.video, name='video'),
    path('video_playing/<str:slug>', views2.video_playing, name='video_playing'),
    path('playlists/', views2.playlists, name='playlists'),
    path('playlist/<str:slug>', views2.plvideos, name='video_in_playlist'),
    path('like_video/<int:pk>/', views2.like_video, name='like_video'),
    path('comment_video/<int:pk>/', views2.comment_video, name='comment_video'),
]
