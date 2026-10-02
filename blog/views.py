from django.core.paginator import EmptyPage,Paginator, PageNotAnInteger 
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

# Create your views here.

class PostListView(ListView):
    """
    Visualização alternativa da lista de posts
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    

"""
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
"""


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


def post_share(request, post_id):
    # Recuperar postagem pelo id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    
    sent = False
    
    if request.method == 'POST':
        # Formulario foi submetido
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Campos do formulário passaram na validação
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recomenda que você leia {post.title}"
            )
            message = (
                f"Leia {post.title} em {post_url}\n\n"
                f"{cd['name']}\'s comentários: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
            # ... enviar e-mail
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )