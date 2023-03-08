from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator

from .models import Post, Group, User

from .forms import PostForm

from .utils import get_paginator

ITS_PER_PG = 10


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = get_paginator(request, post_list)
    context = {
        "paginator": paginator,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = get_paginator(request, post_list)
    context = {
        'group': group,
        'paginator': paginator,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username = username)
    post_list = Post.objects.filter(
        author=author).order_by('-pub_date')
    paginator = get_paginator(request, post_list)
    post_count = post_list.count()
    context = {
        "author": author,
        'username': username,
        'paginator': paginator,
        'post_count': post_count,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk = post_id)
    context = {
        'post':post,
    }
    return render(request, template, context)

@login_required
def post_create(request):
    template = 'post/create_post.html'
    form = PostForm(request.POST or None)
    context = {
        'form': form,
        'username': request.user,
    }
    if form.is_valid():
        post_create = form.save(commit=False)
        post_create.author = request.user
        post_create.save()
        return redirect('posts:profile', username=post_create.author)
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = PostForm(request.POST, instance=post)
    if request.user.id  != post.author.id:
        return redirect('posts:post_detail', post_id=post.id)
    elif form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts: post_detail', post_id= post.id)
    form = PostForm(instance = post)
    context = {
            'form': form,
            'is_edit': True,
            'post': post,
        }
    return redirect(request, 'posts:post_create.html', context)