from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm


def list_posts(request):
    post_list = Post.objects.all()
    context = {'post_list': post_list}
    return render(request, 'receitas/index.html', context)

def detail_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'receitas/details.html', context)

def search_posts(request):
    context = {}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        post_list = Post.objects.filter(name__icontains=search_term)
        context = {"post_list": post_list}
    return render(request, 'receitas/search.html', context)

def create_post(request):
    if request.method == 'POST':
        post_name = request.POST['name']
        post_desc = request.POST['desc']
        post_ingredientes = request.POST['ingredientes']
        post_modo_de_preparo = request.POST['modo_de_preparo']
        post_foto_url = request.POST['foto_url']
        post = Post(name=post_name,
                    desc = post_desc,
                    ingredientes = post_ingredientes,
                    modo_de_preparo = post_modo_de_preparo,
                    foto_url = post_foto_url
                    )
        post.save()
        return HttpResponseRedirect(
            reverse('receitas:details', args=(post.id, )))
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'receitas/create.html', context)
    
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post.name = form.cleaned_data['name']
            post.release_year = form.cleaned_data['release_year']
            post.poster_url = form.cleaned_data['poster_url']
            post.save()
            return HttpResponseRedirect(
                reverse('receitas:details', args=(post.id, )))
    else:
        form = PostForm(
            initial={
                'name': post.name,
                'ingredientes': post.ingredientes,
                'desc': post.desc,
                'modo de preparo':post.modo_de_preparo,
                'foto url':post.foto_url,
            })

    context = {'post': post, 'form': form}
    return render(request, 'receitas/update.html', context)


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse('receitas:index'))

    context = {'post': post}
    return render(request, 'receitas/delete.html', context)
