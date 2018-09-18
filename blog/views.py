from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def index(request):
    keywords1 = request.GET.get("keyword1")
    keywords2 = request.GET.get("keyword2")
    if keywords1 is None and keywords2 is None:
        posts = Post.objects.filter(
            published_date__lte=timezone.now()
        ).order_by('-published_date')
        return render(request, 'blog/index.html', {'posts': posts})

    if keywords2 is None:
        search_posts = Post.objects.filter(
            title__contains=keywords1, text__contains=keywords1
        ).order_by('-published_date')
        return render(request, 'blog/index.html', {'posts': search_posts})

    search_posts = Post.objects.filter(
        Q(title__contains=keywords2) | Q(text__contains=keywords2)
    ).order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': search_posts})

@login_required
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:detail', pk=post.pk)
    
    else:
        form = PostForm()

    return render(request, 'blog/create.html', {'form': form})

@login_required
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:detail', pk=post.pk)
    
    else:
        form = PostForm(instance=post)
        
    return render(request, 'blog/edit.html', {'form': form})

@login_required
def delete(request, pk):
    post = Post.objects.filter(pk=pk).delete()
    return render(request, 'blog/delete.html', {'post': post})

