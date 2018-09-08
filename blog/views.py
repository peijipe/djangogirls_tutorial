from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm


def index(request):
    title = request.GET.get("title")
    if title is None:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'blog/index.html', {'posts': posts})

    search_posts = Post.objects.filter(title__contains=title).order_by('published_date')
    return render(request, 'blog/index.html', {'posts': search_posts})
    
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})
    
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

def delete(request, pk):
    post = Post.objects.filter(pk=pk).delete()
    return render(request, 'blog/delete.html', {'post': post})