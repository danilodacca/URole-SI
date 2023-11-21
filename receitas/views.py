from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm
from django.views import generic


class PostsListView(generic.ListView):
    model = Post
    template_name = 'receitas/index.html'

class PostsDetailView(generic.DetailView):
    model = Post
    template_name = 'receitas/details.html'
    context_object_name = 'post'


class PostsCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'receitas/create.html'
    success_url = '/receitas/'
    


class PostsUpdateView(generic.UpdateView):
    model = Post
    template_name = 'receitas/update.html'
    fields = ['name', 'ingredientes','desc','modo_de_preparo','foto_url' ]
    success_url = '/receitas/'

class PostsDeleteView(generic.DeleteView):
    model = Post
    template_name = 'receitas/delete.html'
    success_url = '/receitas'
