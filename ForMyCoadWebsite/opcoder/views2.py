from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from math import ceil as c
import random
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# For video and profile logic.

def show_videos(request, videos):
    no_of_videos = 12
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    length = len(videos)
    # videos = random.sample(videos, length)
    videos = videos[(page-1)*no_of_videos: page*no_of_videos]
    if page > 1:
        prev = page-1
    else:
        prev = None
    if page < c(length/no_of_videos):
        nxt = page + 1
    else:
        nxt = None
    context = {'videos': videos, 'prev': prev, 'nxt': nxt}
    return render(request, "opcoder/videos.html", context)
def video(request):
    videos = Video.objects.all()
    return show_videos(request, videos)


def plvideos(request, slug):
    videos = Video.objects.filter(playlist__slug=slug)
    return show_videos(request, videos)


def playlists(request):
    all_playlists = Playlist.objects.all()
    return render(request, "opcoder/playlist.html", {'playlists':all_playlists})


def video_playing(request, slug):
    video_found = Video.objects.filter(slug=slug).first()

    if video_found:
        video_found.tviews += 1
        video_found.save()

    pl_videos = 'None'
    if video_found.playlist:
        pl_videos = Video.objects.filter(playlist=video_found.playlist)

    mvideos = list(Video.objects.all())
    more_videos = random.sample(mvideos, len(mvideos))

    context = {'name': video_found, 'types':video_found.source[8:23], 'plvideos':pl_videos, 'mvideos':more_videos}
    return render(request, "opcoder/video_playing.html", context)


@login_required(login_url='/login/')
@require_POST
def like_video(request, pk):
    video_found = get_object_or_404(Video, sno=pk)
    video_found.tlikes += 1
    video_found.save()

    return JsonResponse({
        'likes_count': video_found.tlikes,
        'message': 'Like recorded successfully'
    })


@login_required(login_url='/login/')
@require_POST
def comment_video(request, pk):
    try:
        data = json.loads(request.body)
        comment_body = data.get('comment_body')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    if not comment_body:
        return JsonResponse({'error': 'Comment body is empty'}, status=400)

    video_post = get_object_or_404(Video, sno=pk)
    user = request.user

    new_comment = VideoComment.objects.create(video=video_post, name=user, body=comment_body)

    return JsonResponse({
        'success': True,
        'comment_body': new_comment.body,
        'comment_name': new_comment.name.username,
        'comment_date': new_comment.date.strftime("%d-%m-%Y")}, status=201)
