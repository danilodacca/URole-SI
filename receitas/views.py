from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Role, Category
from .forms import RoleForm
from django.views import generic

def staff_required(user):
    return user.is_authenticated and  user.is_staff

def user_login_required(user):
    return user.is_authenticated

def is_user(user):
    return not user.is_staff

class RolesListView(generic.ListView):
    model = Role
    template_name = 'receitas/index.html'

class PostsDetailView(generic.DetailView):
    model = Role
    template_name = 'receitas/details.html'
    context_object_name = 'role'

def search_roles(request):
    context = {}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        role_list = Role.objects.filter(name__icontains=search_term)
        context = {"role_list": role_list}
    return render(request, 'receitas/search.html', context)

@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class PostsCreateView(generic.CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'receitas/create.html'
    success_url = '/receitas/'
    
@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class PostsUpdateView(generic.UpdateView):
    model = Role
    template_name = 'receitas/update.html'
    fields = ['name', 'date', 'start_time', 'end_time', 'address', 'banner_url', 'about']
    success_url = '/receitas/'

@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class PostsDeleteView(generic.DeleteView):
    model = Role
    template_name = 'receitas/delete.html'
    success_url = '/receitas/'

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'receitas/categories.html'


class CategoryCreateView(generic.CreateView):
    model = Category
    template_name = 'receitas/create_category.html'
    fields = ['name', 'author', 'roles']
    success_url = reverse_lazy('receitas:categories')

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'receitas/category.html'
    context_object_name = 'category'