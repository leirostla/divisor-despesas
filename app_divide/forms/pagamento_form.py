from django import forms

from app_divide.models import Pagamento

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ('despesa', 'pagador', 'valor_pago')
        labels = {
            'despesa': 'Despesa',
            'pagador': 'Pagador',
            'valor_pago': 'Valor Pago',
        }
        widgets = {
            'despesa': forms.Select(attrs={
                'class': 'form-control',
            }),
            'pagador': forms.Select(attrs={
                'class': 'form-control',
            }),
            'valor_pago': forms.NumberInput(attrs={
                'placeholder': '0,00',
                'min': '0.01',
                'step': '0.01',
                'class': 'form-control',
            }),
        }

    def clean_valor_pago(self):
        valor = self.cleaned_data['valor_pago']
        if valor <= 0:
            raise forms.ValidationError('Informe um valor maior que zero.')
        return valor