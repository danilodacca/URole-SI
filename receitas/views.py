from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.shortcuts import render, get_object_or_404


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
        return render(request, 'receitas/create.html', {})
    
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        post.name = request.POST['name']
        post.desc = request.POST['desc']
        post.ingredientes = request.POST['ingredientes']
        post.modo_de_preparo = request.POST['modo_de_preparo']
        post.foto_url = request.POST['foto_url']
        post.save()
        return HttpResponseRedirect(
            reverse('receitas:details', args=(post.id, )))

    context = {'post': post}
    return render(request, 'receitas/update.html', context)


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse('receitas:index'))

    context = {'post': post}
    return render(request, 'receitas/delete.html', context)
