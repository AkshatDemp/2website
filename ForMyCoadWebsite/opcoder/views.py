from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from math import ceil as c
from .models import *

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request, "opcoder/index.html")

def search(request):
    a = (request.GET.get("slug"))
    longblogs = Blog.objects.filter(slug=a).first()
    print(longblogs)
    longblogslist = {'name': longblogs}
    return render(request, 'opcoder/blogpost.html', longblogslist)

def profile(request):
    return render(request, "opcoder/profile.html")

def show_blog(request, blogs):
    no_of_posts = 6
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    length = len(blogs)
    blogs = blogs[(page-1)*no_of_posts: page*no_of_posts]
    if page > 1:
        prev = page-1
    else:
        prev = None
    if page < c(length/no_of_posts):
        nxt = page + 1
    else:
        nxt = None
    context = {'blogs': blogs, 'prev': prev, 'nxt': nxt}
    return render(request, 'opcoder/blogs.html', context)

def blog(request):
    blogs = Blog.objects.all().order_by('-time')
    return show_blog(request, blogs)

def blogpost(request, slug):
    this_blog = Blog.objects.filter(slug=slug).first()
    context = {'post': this_blog}
    if this_blog:
        this_blog.views += 1
        this_blog.save()

    return render(request, 'opcoder/blogpost.html', context)

@login_required(login_url='/login/')
@require_POST
def like_blog_post(request, pk):
    blog_post = get_object_or_404(Blog, sno=pk)
    blog_post.likes += 1
    blog_post.save()

    return JsonResponse({
        'likes_count': blog_post.likes,
        'message': 'Like recorded successfully'
    })

@login_required(login_url='/login/')
@require_POST
def add_comment(request, pk):
    try:
        data = json.loads(request.body)
        comment_body = data.get('comment_body')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    if not comment_body:
        return JsonResponse({'error': 'Comment body is empty'}, status=400)

    blog_post = get_object_or_404(Blog, sno=pk)
    user = request.user

    new_comment = BlogComment.objects.create(blog=blog_post, name=user, body=comment_body)

    return JsonResponse({
        'success': True,
        'comment_body': new_comment.body,
        'comment_name': new_comment.name.username,
        'comment_date': new_comment.date.strftime("%d-%m-%Y")}, status=201)
