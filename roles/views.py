from typing import Any
from django.db import models
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .models import Role, Ticket
from .forms import RoleForm, TicketForm
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

@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class TicketsCreateView(generic.CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'roles/create_ticket.html'
    def get_success_url(self):
        print(self.kwargs)
        return reverse("roles:tickets", kwargs={'pk': self.kwargs['pk']})
    def form_valid(self, form):
        form.instance.role = Role.objects.filter(id=self.kwargs['pk'])[0]
        return super().form_valid(form)

@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class TicketsUpdateView(generic.UpdateView):
    model = Ticket
    template_name = 'roles/update_ticket.html'
    fields = ['type', 'price']
    lookup_field='id'
    def get_success_url(self):
        return reverse("roles:tickets", kwargs={"pk": self.kwargs['pk']})
    def get_object(self):
        return Ticket.objects.all().filter(role__id=self.kwargs['pk']).get(type=self.kwargs['type'])

@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class TicketsDeleteView(generic.DeleteView):
    model = Ticket
    template_name = 'roles/delete_ticket.html'
    def get_success_url(self):
        return reverse("roles:tickets", kwargs={"pk": self.kwargs['pk']})
    def get_object(self):
        return Ticket.objects.all().filter(role__id=self.kwargs['pk']).get(type=self.kwargs['type'])

def TicketsListView(request, pk):
    ticket_list = Ticket.objects.filter(role=Role.objects.get(id=pk)).values_list('type','price', named=True)
    return render(request,"roles/tickets.html", context={'ticket_list': ticket_list, 'pk_role':pk})

def MyTicketsListView(request):
    ticket_list = Ticket.objects.filter(owner=request.user).values_list('type','price', named=True)
    return render(request,"roles/mytickets.html", context={'ticket_list': ticket_list})

@method_decorator(user_passes_test(is_user, login_url='/accounts/login'), name='dispatch')
class TicketsBuyView(generic.CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'roles/create_ticket.html'
    def get_success_url(self):
        return reverse("roles:tickets", kwargs={'pk': self.kwargs['pk']})
    def form_valid(self, form):
        form.instance.role = Role.objects.filter(id=self.kwargs['pk'])[0]
        return super().form_valid(form)
