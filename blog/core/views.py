from django.shortcuts import render
from .models import Post
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #três postagens por página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira pagina
        posts = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo
        # Exibe a ultima pagina de resultados
        posts = paginator.page(paginator.num_pages)
    return render(request, 'core/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', 
    publish__year=year, publish__month=month, publish__day=day)
    
    return render(request, 'core/post/detail.html', {'post': post})

