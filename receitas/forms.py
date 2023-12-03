from django import forms
from django.forms import ModelForm
from .models import Role

class RoleForm(forms.ModelForm):
    banner_url = forms.URLField(label='URL do banner')
    class Meta:
        model = Role
        fields = ('name', 'date', 'start_time', 'end_time', 'address', 'banner_url', 'about')
        labels = {
            'name':'Nome do rolê',
            'date':'Data',
            'start_time':'Horário de Início',
            'end_time':'Horário do Fim',
            'address':'Endereço',
            'banner_url':'URL do banner do evento',
            'about':'Descrição e Informações'
        }
        widgets = {
                'date': forms.DateInput(attrs={'type': 'date'}),
                'start_time':forms.TimeInput(attrs={'type': 'time'}),
                'end_time':forms.TimeInput(attrs={'type': 'time'}),
            }

    def __str__(self):
        return self.name