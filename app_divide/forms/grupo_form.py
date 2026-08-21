from django import forms
from app_divide.models import Grupo

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'descricao']
        labels = {'nome':"Nome",
                  'descricao': 'Descrição'}
        widget = {
            'nome': forms.TextInput(attrs={'autofocus':True}),
            'descricao': forms.Textarea(attrs={'rows': 3})
            }