from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def index(request):
    and_keywords = request.GET.get("keyword1")
    or_keywords = request.GET.get("keyword2")

    if and_keywords:
        and_key_list = and_keywords.replace('　', ' ').split(' ')

        # 全件取得
        search_posts = Post.objects.all()

        for data in and_key_list:
            search_posts = search_posts.filter(title__contains=data, text__contains=data)

        search_posts = search_posts.order_by('-published_date')
        return render(request, 'blog/index.html', {'posts': search_posts, 'and_keywords': and_keywords})

    if or_keywords:
        or_key_list = or_keywords.replace('　', ' ').split(' ')
        queries = [Q(title__contains=key) | Q(text__contains=key) for key in or_key_list]
        print(queries)
        query = queries.pop()
        for item in queries:
            query |= item
        print(query)
        search_posts = Post.objects.filter(query).order_by('-published_date')
        return render(request, 'blog/index.html', {'posts': search_posts, 'or_keywords': or_keywords})

    search_posts = Post.objects.all().order_by('-published_date')
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

