from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Role
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
    template_name = 'roles/index.html'

class PostsDetailView(generic.DetailView):
    model = Role
    template_name = 'roles/details.html'
    context_object_name = 'role'

def search_roles(request):
    context = {}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        role_list = Role.objects.filter(name__icontains=search_term)
        context = {"role_list": role_list}
    return render(request, 'roles/search.html', context)

@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class PostsCreateView(generic.CreateView):
    model = Role
    form_class = RoleForm
    template_name = 'roles/create.html'
    success_url = '/roles/'
    
@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class PostsUpdateView(generic.UpdateView):
    model = Role
    template_name = 'roles/update.html'
    fields = ['name', 'date', 'start_time', 'end_time', 'address', 'banner_url', 'about']
    success_url = '/roles/'

@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class PostsDeleteView(generic.DeleteView):
    model = Role
    template_name = 'roles/delete.html'
    success_url = '/roles/'
