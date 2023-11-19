from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Receita
from django.shortcuts import render, get_object_or_404


def list_receitas(request):
    receita_list = Receita.objects.all()
    context = {'receita_list': receita_list}
    return render(request, 'receitas/index.html', context)

def detail_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    context = {'receita': receita}
    return render(request, 'receitas/detail.html', context)

def search_receitas(request):
    context = {}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        receita_list = Receita.objects.filter(name__icontains=search_term)
        context = {"receita_list": receita_list}
    return render(request, 'receitas/search.html', context)

def create_receita(request):
    if request.method == 'POST':
        receita_name = request.POST['name']
        receita_ingredientes = request.POST['ingredientes']
        receita_modo_de_preparo = request.POST['modo_de_preparo']
        receita_foto_url = request.POST['foto_url']
        receita = Receita(name=receita_name,
                      ingredientes = receita_ingredientes,
                      modo_de_preparo = receita_modo_de_preparo,
                      foto_url = receita_foto_url
                      )
        receita.save()
        return HttpResponseRedirect(
            reverse('receitas:detail', args=(receita.id, )))
    else:
        return render(request, 'receitas/create.html', {})
    
