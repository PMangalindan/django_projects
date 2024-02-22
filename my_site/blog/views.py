from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
all_posts = []
# Create your views here.
def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/index.html", {"posts": latest_posts})
def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-post.html", {"posts": all_posts})
def post_detail(request, slug):
    current_post = get_object_or_404(Post, slug = slug)
    request.session["current_post_path"] = request.path
    try:
        stored_post = request.session.get("stored_posts")
    except:
        stored_post = []
    request.session["recent_visited_post"] = current_post.title ## for adding to read_later_list
    #stored_post.append(current_post.title )
    #stored_post = list(dict(stored_post))
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.has_changed():
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = current_post
                comment.save()
                return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
            else:
                return render(request, "blog/post-detail.html", {"posts": current_post, "comment_form": comment_form, "comments": current_post.comments.all().order_by("-id"), "stored_posts": stored_post})
        else:
            comment_form = CommentForm()
            return render(request, "blog/post-detail.html", {"posts": current_post, "comment_form": comment_form, "comments": current_post.comments.all().order_by("-id"), "stored_posts": stored_post})
    except:
        comment_form = CommentForm()
        return render(request, "blog/post-detail.html", {"posts": current_post, "comment_form": comment_form, "comments": current_post.comments.all().order_by("-id"), "stored_posts": stored_post})
"""def read_later(request):
    try:
        try:
            stored_post = request.session.get("stored_post")
        except:
            stored_post = None
        if stored_post is None:
            stored_post = []
        print(stored_post)
        post_id = request.POST["post_id"]
        if post_id not in stored_post:
            stored_post.append(post_id)
            request.session["stored_posts"] = stored_post
    except:
        pass
    return HttpResponseRedirect("/")"""
def read_later(request):
    current_post_path = request.session.get("current_post_path")
    to_read_later_post = request.session.get("recent_visited_post")
    try:
        stored_post = request.session.get("stored_posts")
    except:
        stored_post = []
    if stored_post == None:
        stored_post = []
    if to_read_later_post not in stored_post:
            stored_post.append(to_read_later_post)
            request.session["stored_posts"] = stored_post
            return HttpResponseRedirect(current_post_path)
    else:
        return HttpResponseRedirect("/read-later-list")
def read_later_list(request):
    stored_post = request.session.get("stored_posts")
    print(stored_post)
    all_posts = Post.objects.all()
    return render(request, "blog/stored-posts.html", {"stored_post": stored_post, "posts" : all_posts })