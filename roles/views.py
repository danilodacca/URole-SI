from django.urls import reverse
from django.shortcuts import render
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .models import Role, Ticket
from .forms import RoleForm, TicketForm
from django.views import generic

def staff_required(user):
    return user.is_authenticated and  user.is_staff

def user_login_required(user):
    return user.is_authenticated

def user_required(user):
    return user.is_authenticated and not user.is_staff

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
        return reverse("roles:tickets", kwargs={'pk': self.kwargs['pk']})
    def form_valid(self, form):
        form.instance.role = Role.objects.filter(id=self.kwargs['pk'])[0]
        self.object = form.save()
        form.instance.owner.add(self.request.user)
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
        return Ticket.objects.all().filter(role__id=self.kwargs['pk']).get(id=self.kwargs['id'])

@method_decorator(user_passes_test(staff_required, login_url='/accounts/login'), name='dispatch')
class TicketsDeleteView(generic.DeleteView):
    model = Ticket
    template_name = 'roles/delete_ticket.html'
    def get_success_url(self):
        return reverse("roles:tickets", kwargs={"pk": self.kwargs['pk']})
    def get_object(self):
        return Ticket.objects.all().filter(role__id=self.kwargs['pk']).get(id=self.kwargs['id'])

def TicketsListView(request, pk):
    ticket_list = Ticket.objects.filter(role=Role.objects.get(id=pk)).exclude(owner=request.user.id).filter(on_sale=True)
    staff_list = [ticket.id for ticket in ticket_list.exclude(owner__is_staff=False)]
    ticket_list = ticket_list.values_list('type','price', 'id', 'owner', named=True)
    print(staff_list)
    print(ticket_list)
    return render(request,"roles/tickets.html", context={'ticket_list': ticket_list, 'pk_role':pk, 'staff_list': staff_list})


def MyTicketsListView(request):
    ticket_list = Ticket.objects.filter(owner=request.user.id).values_list('type','price', 'id', 'on_sale', named=True)
    return render(request,"roles/mytickets.html", context={'ticket_list': ticket_list})

def TicketsBuyView(request, pk, id):
    print(request.__dict__)
    ticket = Ticket.objects.all().filter(role__id=pk).get(id=id)
    if ticket.owner.all()[0].is_staff:
        return TicketsBuyFromStaffView().as_view()(request)
    else:
        return TicketsBuyFromUserView().as_view()(request)

@method_decorator(user_passes_test(user_required, login_url='/accounts/login'), name='dispatch')
class TicketsBuyFromStaffView(generic.CreateView):
    model = Ticket
    template_name = 'roles/buy_ticket.html'
    fields = []
    lookup_field='id'
    def get_success_url(self):
        return reverse("roles:mytickets")
    def form_valid(self, form):
        ticket = Ticket.objects.all().filter(role__id=self.kwargs['pk']).get(id=self.kwargs['id'])
        form.instance.type = ticket.type
        form.instance.role = Role.objects.filter(id=self.kwargs['pk'])[0]
        form.instance.price = ticket.price
        form.instance.on_sale = False
        form.save()
        form.instance.owner.add([self.request.user])
        return super().form_valid(form)
    def get_object(self):
        return Ticket.objects.all().filter(role__id=self.kwargs['pk']).get(id=self.kwargs['id'])

@method_decorator(user_passes_test(user_required, login_url='/accounts/login'), name='dispatch')
class TicketsBuyFromUserView(generic.UpdateView):
    model = Ticket
    template_name = 'roles/buy_ticket.html'
    fields = []
    lookup_field='id'
    def get_success_url(self):
        return reverse("roles:mytickets")
    def form_valid(self, form):
        form.instance.on_sale = False
        #form.instance.owner.set([None])
        form.save()
        form.instance.owner.set([self.request.user])
        return super().form_valid(form)
    def get_object(self):
        return Ticket.objects.all().get(id=self.kwargs['id'])

@method_decorator(user_passes_test(user_required, login_url='/accounts/login'), name='dispatch')
class TicketsSellView(generic.UpdateView):
    model = Ticket
    template_name = 'roles/sell_ticket.html'
    fields = ['price']
    lookup_field='id'
    def get_success_url(self):
        return reverse("roles:mytickets")
    def form_valid(self, form):
        form.instance.on_sale = True
        return super().form_valid(form)
    def get_object(self):
        return Ticket.objects.all().get(id=self.kwargs['id'])

@method_decorator(user_passes_test(user_required, login_url='/accounts/login'), name='dispatch')
class TicketsCancelSellView(generic.UpdateView):
    model = Ticket
    template_name = 'roles/cancelsell_ticket.html'
    fields = []
    lookup_field='id'
    def get_success_url(self):
        return reverse("roles:mytickets")
    def form_valid(self, form):
        form.instance.on_sale = False
        return super().form_valid(form)
    def get_object(self):
        return Ticket.objects.all().get(id=self.kwargs['id'])
