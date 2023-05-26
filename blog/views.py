from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,\
    PageNotAnInteger

from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm

from django.core.mail import send_mail

from django.views.decorators.http import require_POST


# Class Based view
class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# Create your views here.


def post_list(request):
    post_list = Post.objects.all()

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        # If page number is out of range
        #   deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post)

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    # Form for users to comment
    form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {"post": post,
                   'comments': comments,
                   'form': form})

# This function recommends posts to user


def post_share(request, post_id):
    # sourcery skip: extract-method, inline-variable
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == 'POST':
        # Form submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Send email

            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read "\
                      f"{post.title}"
            message = f"{post.title} Onek joss!"
            my_mail = "dxxdphantom@gmail.com"

            send_mail(subject, message, my_mail, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})


# This is for commenting
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None

    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment = form.save(commit=False)

        # Assign the post to the comment
        comment.post = post

        # Save the comment to the database
        comment.save()

    return render(request, 'blog/post/comment.html',
                  {
                      'post': post,
                      'form': form,
                      'comment': comment
                  })
