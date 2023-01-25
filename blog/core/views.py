from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from taggit.models import Tag

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


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts por página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página
        posts = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do inervalo, exibe a ultima página de resultados
        posts = paginator.page(paginator.num_pages)
    return render(request, 'core/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


class PostListView(ListView):
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

