from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm
from django.views import generic


class PostListView(generic.ListView):
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


class PostsUpdateView(generic.UpdateView):
    model = Post
    template_name = 'receitas/update.html'

class PostsDeleteView(generic.DeleteView):
    model = Post
    template_name = 'receitas/delete.html'
