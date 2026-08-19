from django import forms

from app_divide.models import Despesa


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ('descricao', 'valor_total', 'observacao')
        labels = {
            'descricao': 'Descrição',
            'valor_total': 'Valor',
            'observacao': 'Observação',
        }
        widgets = {
            'descricao': forms.TextInput(attrs={
                'placeholder': 'Ex.: Jantar',
                'autofocus': True,
            }),
            'valor_total': forms.NumberInput(attrs={
                'placeholder': '0,00',
                'min': '0.01',
                'step': '0.01',
            }),
            'observacao': forms.Textarea(attrs={
                'placeholder': 'Informações adicionais (opcional)',
                'rows': 3,
            }),
        }

    def clean_valor_total(self):
        valor = self.cleaned_data['valor_total']
        if valor <= 0:
            raise forms.ValidationError('Informe um valor maior que zero.')
        return valor
