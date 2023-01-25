from django.shortcuts import render
from django.views.generic import ListView

from .models import Post
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', 
    publish__year=year, publish__month=month, publish__day=day)
    
    return render(request, 'core/post/detail.html', {'post': post})


class PostListView(ListView):
    queryset = Post.published.all().filter(publish__year='2023')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'core/post/list.html'

