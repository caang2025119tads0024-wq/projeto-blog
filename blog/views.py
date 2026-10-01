from django.core.paginator import EmptyPage,Paginator, PageNotAnInteger 
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404

# Create your views here.

def post_list(request):
    post_list = Post.published.all()
    # Paginação com 3 posts por página
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        #Se o número_da_página estiver fora do intervalo, pega a última página dos resultados
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #Se o número_da_página não for um inteiro, pega a primeira página dos resultados
        posts = paginator.page(1)
    except EmptyPage:
        #Se o número_da_página estiver fora do intervalo, pega a última página dos resultados
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'posts':posts}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
      Post,
      status=Post.Status.PUBLISHED,
      slug=post,
      publish__year=year,
      publish__month=month,
      publish__day=day)
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
