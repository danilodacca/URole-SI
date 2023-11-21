from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
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

def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_author = form.cleaned_data['author']
            comment_text = form.cleaned_data['text']
            comment = Comment(author=comment_author,
                            text=comment_text,
                            post=post)
            comment.save()
            return HttpResponseRedirect(
                reverse('receitas:detail', args=(post_id, )))
    else:
        form = CommentForm()
    context = {'form': form, 'comment': comment}
    return render(request, 'receitas/comment.html', context)
