from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Image, Comment, Hashtag
from .forms import PostForm, ImageForm, CommentForm
from django.contrib.auth.decorators import login_required

from django.db.models import Q

# from itertools import chain


# Create your views here.
@login_required
def list(request):
    # posts = get_list_or_404(Post.objects.order_by('-pk'))
    # posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-pk')
    followings = request.user.followings.all()
    # 팔로워와 내가 작성한 글만 읽기 1번
    posts = Post.objects.filter(Q(user__in=followings) | Q(user = request.user.id)).order_by('-pk')
    # 팔로워와 내가 작성한 글만 읽기 2번
    # chain_followings = chain(followings, [request.user])
    # posts = Post.objects.filter(user__in=chain_followings).order_by('-pk')
    comment_form = CommentForm()
    
    context = {
        'posts': posts,
        'comment_form':comment_form,
    }
    return render(request, 'posts/list.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)    # 게시글 내용 처리 끝
            post.user = request.user
            post.save()
            # hashtag - post의 content 를 사용해야하기 때문에 post.save()가 된 이후에 hashtag 코드가 와야함.
            for word in post.content.split():
                if word[0] == "#":
                # if word.startswith('#'):
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    # (Hashtag의 인스턴스, boolean)인 튜플형식으로 출력됨
                    post.hashtags.add(hashtag[0])
                    
            # 1. 게시글을 순회하면서 띄어쓰기를 잘라야함
            # 2. 자른 단어가 # 으로 시작하나?
            # 3. 이 해시 태그가 기존 해시태그에 있는 건지?
            
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
            
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form' : post_form,
        'image_form' : image_form,
        }
    return render(request, 'posts/form.html', context)

@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user != request.user:
        return redirect('posts:list')
        
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)  # 1
        if post_form.is_valid():
            post = post_form.save()                         # 2
            
            # hashtag update
            post.hashtags.clear()
            for word in post.content.split():
                if word[0] == "#":
                # if word.startswith('#'):
                    hashtag = Hashtag.objects.get_or_create(content=word)
                    # (Hashtag의 인스턴스, boolean)인 튜플형식으로 출력됨
                    post.hashtags.add(hashtag[0])
            return redirect('posts:list')
            
    else:
        post_form = PostForm(instance=post)                 # 3
    context = {
        'post_form' : post_form,
    }
    return render(request, 'posts/form.html', context)


def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user != request.user:
        return redirect('posts:list')
        
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')

@login_required
@require_POST
def comment_create(request, post_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_pk
        comment.save()
    return redirect('posts:list')
    # else:
    #     form = CommentForm()
    # context = {
    #     'form':form,
    # }
    # return render(request,'posts/form.html', context)

def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.user:
        return redirect('posts:list')
        
    if request.method == 'POST':
        comment.delete()
    return redirect('posts:list')
    
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 이미 해당 유저가 like_users 에 존재하면 해당 유저를 삭제

    #1번 방식
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    
    # 없으면 추가(좋아요)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
    
    
    # # 2번 방식
    # user = request.user
    # if post.like_users.filter(pk=user.pk).exists():
    #     post.like_users.remove(user)
    # else:
    #     post.like_users.add(user)
    # return redirect('posts:list')
    
@login_required
def explore(request):
    posts = Post.objects.order_by('-pk')
    posts = Post.objects.exclude(user=request.user).order_by('-pk')
    comment_form = CommentForm()
    context ={
        'posts':posts,
        'comment_form':comment_form,
    }
    return render(request,'posts/explore.html', context)
    
def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    posts = hashtag.post_set.order_by('-pk')
    context = {
        'hashtag':hashtag,
        'posts':posts,
    }
    return render(request, 'posts/hashtag.html', context)