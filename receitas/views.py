from django.http import HttpResponse
from .temp_data import receita_data
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def list_receitas(request):
    context = {"receita_list": receita_data}
    return render(request, 'receitas/index.html', context)

def detail_receita(request, receita_id):
    context = {'receita': receita_data[receita_id - 1]}
    return render(request, 'receitas/details.html', context)

def search_receitas(request):
    context = {}
    if request.GET.get('query', False):
        context = {
            "receita_list": [
                m for m in receita_data
                if request.GET['query'].lower() in m['name'].lower()
            ]
        }
    return render(request, 'receitas/search.html', context)

def create_receita(request):
    if request.method == 'POST':
        receita_data.append({
            'name': request.POST['name'],
            'release_year': request.POST['release_year'],
            'poster_url': request.POST['poster_url']
        })
        return HttpResponseRedirect(
            reverse('receitas:detail', args=(len(receita_data), )))
    else:
        return render(request, 'receitas/create.html', {})