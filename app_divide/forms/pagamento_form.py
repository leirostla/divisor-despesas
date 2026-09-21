from django import forms

from app_divide.models import Pagamento, Despesa, ParticipanteGrupo


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
                'class': 'form-select',
            }),
            'pagador': forms.Select(attrs={
                'class': 'form-select',
            }),
            'valor_pago': forms.NumberInput(attrs={
                'placeholder': '0,00',
                'min': '0.01',
                'step': '0.01',
                'class': 'form-control',
                'required': True,
            }),
        }

    def __init__(self, *args, grupo=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['pagador'].label_from_instance = self.nome_pagador
        self.fields['pagador'].empty_label = "Selecione um pagador"
        
        self.fields["despesa"].empty_label = (
            "Selecione uma despesa"
        )

        if grupo is None:
            self.fields['despesa'].queryset = Despesa.objects.none()
            self.fields['pagador'].queryset = ParticipanteGrupo.objects.none()
        else:
            self.fields['despesa'].queryset = Despesa.objects.filter(
                grupo=grupo).order_by('-data_despesa', '-pk')
            self.fields['pagador'].queryset = ParticipanteGrupo.objects.filter(
                grupo=grupo, ativo=True).select_related('usuario').order_by('usuario__first_name', 'usuario__username')

    def nome_pagador(self, participante):
        return f"{participante.usuario.first_name} ({participante.usuario.username})"

    def clean_valor_pago(self):
        valor = self.cleaned_data['valor_pago']
        if valor <= 0:
            raise forms.ValidationError('Informe um valor maior que zero.')
        return valor
