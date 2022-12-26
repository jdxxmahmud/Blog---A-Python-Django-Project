from django.shortcuts import render, get_object_or_404
from .models import Post
import datetime

from django.http import Http404
# Create your views here.


def post_list(request):
    posts = Post.objects.all()
    timeNow = datetime.datetime.now()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'date': datetime.date.today(),
                   'time': timeNow.strftime("%I:%M %p")})


def post_detail(request, id):
    timeNow = datetime.datetime.now()
    post = get_object_or_404(Post,
                             id=id)

    return render(request,
                  'blog/post/detail.html',
                  {"post": post,
                   'date': datetime.date.today(),
                   'time': timeNow.strftime("%I:%M %p")})
