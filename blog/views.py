from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views import View

from blog.tasks import send_email_comment
from account.models import User
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment


class PostCreate(View):

    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_verificate:
            raise Http404('Register, please.')
        form = PostForm()
        context = {'form': form}
        return render(request, 'blog/create_post.html', context)

    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_verificate:
            raise Http404('Register, please.')
        context = {}
        if request.method == "POST":
            form = PostForm(request.POST)
            user = request.user
            if not user.is_authenticated:
                return redirect('/')

            if form.is_valid():
                post_item = form.save(commit=False)
                author = User.objects.filter(email=user.email).first()
                post_item.author = author

                if user.is_staff:
                    post_item.status = 'approve'

                post_item.save()
                return redirect('Posts')
        else:
            form = PostForm()
            context['form'] = form
        return render(request, 'blog/create_post.html', context)


class PostDetailAndComment(View):

    def get(self, request, id):
        if request.method == 'GET':
            post = get_object_or_404(Post, id=id)
            if post.status == 'unview' or post.status == 'decline':
                raise Http404('Post on pre-moderation.')
            comments = Comment.objects.filter(post=post)
            comment_form = CommentForm()
            return render(request, 'blog/post_detail.html', {
                'post': post,
                'comments': comments,
                'comment_form': comment_form
            })

    def post(self, request, id):
        if request.method == 'POST':
            post = Post.objects.get(id__iexact=id)
            user = request.user
            comments = Comment.objects.filter(post=post)
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new = comment_form.save(commit=False)
                new.post = post
                new.author = user
                send_email_comment(post=post.title, email=post.author.email, comment=new.body)
                new.save()
            return render(request, 'blog/post_detail.html', {
                'post': post,
                'comments': comments,
                'comment_form': comment_form
            })


class PostList(View):
    def get(self, request):
        posts = Post.approved.all().order_by('date').reverse()
        context = {
            'posts': posts
        }
        return render(request, 'blog/posts.html', context)


