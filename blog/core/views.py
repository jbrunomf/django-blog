from django.shortcuts import render
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm, CommentForm


# Create your views here.
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # O comentário foi postado
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'core/post/detail.html', {'post': post, 'comments': comments,
                                                     'new_comment': new_comment, 'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all().filter(publish__year='2023')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'core/post/list.html'


def post_share(request, post_id):
    # Obtem a postagem pelo id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        #O formulário foi submetido
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recomendou que você leia {post.title}'
            message = f"Read {post.title} at {post_url}\n\n{cd['name']} comentou: {cd['comments']}"
            send_mail(subject, message, 'admin@blog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'core/post/share.html', {'post': post, 'form': form, 'sent': sent})
