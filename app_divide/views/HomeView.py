from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.db import transaction, IntegrityError 
from django.shortcuts import redirect, render
from django.urls import reverse


from app_divide.forms.despesa_form import DespesaForm
from app_divide.forms.pagamento_form import PagamentoForm
from app_divide.models import Grupo, ParticipanteGrupo, Pagamento

from app_divide.models.participacao_despesa import ParticipacaoDespesa
from app_divide.service.divisao import CalcularPartesDespesa, Divisao


# Create your views here.
def home_view(request):
    return render(request, template_name='home/home.html', status=200)


def sumario_view(request):
    print(f"Request method: {request.method} em sumario_view")
    grupos = Grupo.objects.none()
    pessoas = get_user_model().objects.none()
    grupo_selecionado = None
    despesas = []
    despesa_form = DespesaForm()
    pagamento_form = PagamentoForm()

    if request.user.is_authenticated:
        grupos = (Grupo.objects.annotate(participantes_ativos=Count('participantes', filter=Q(participantes__ativo=True), distinct=True,))
                  .filter(participantes__usuario=request.user, participantes__ativo=True)
                  .distinct()
                  .order_by('nome')
                  )
        pessoas = (
            get_user_model().objects
            .filter(participacoes__grupo__in=grupos, participacoes__ativo=True)
            .exclude(pk=request.user.pk)
            .distinct()
            .order_by('first_name', 'username')
        )

        grupo_id = request.POST.get('grupo') if request.method == 'POST' else request.GET.get('grupo')
        print(f"Grupo_ID selecionado: {grupo_id}")

        if grupo_id and grupo_id.isdigit():
            grupo_selecionado = grupos.filter(pk=grupo_id).first()
        if grupo_selecionado is None:
            grupo_selecionado = grupos.first()

        if grupo_selecionado is not None:
            despesas = (
                grupo_selecionado.grupo_despesa
                .select_related('criador', 'criador__usuario')
                .order_by('-data_despesa', '-pk')
            )
            pessoas = (
                get_user_model().objects
                .filter(participacoes__grupo_id=grupo_selecionado.pk, participacoes__ativo=True)
                .exclude(pk=request.user.pk)
                .distinct()
                .order_by('first_name', 'username')
            )
                        
        if request.method == 'POST':
            despesa_form = DespesaForm(request.POST)
            participante = None
            if grupo_selecionado is not None:
                participante = ParticipanteGrupo.objects.filter(
                    grupo=grupo_selecionado,
                    usuario=request.user,
                    ativo=True,
                ).first()

            if participante is None:
                messages.error(
                    request, 'Você não pode adicionar despesas a este grupo.')
            elif despesa_form.is_valid():
                try:
                    with transaction.atomic():

                        despesa = despesa_form.save(commit=False)
                        despesa.grupo = grupo_selecionado
                        despesa.criador = participante
                        despesa.save()
                        CalcularPartesDespesa().calcular_partes_despesa(despesa, grupo_selecionado, participante, pessoas)

                except IntegrityError as ie:
                    messages.error(request, f'Erro ao adicionar a despesa:{ie}')
                
                messages.success(request, 'Despesa adicionada com sucesso.')
                url = f"{reverse('sumario')}?grupo={grupo_selecionado.pk}"
                return redirect(url)

    context = {
        'grupos': grupos,
        'pessoas': pessoas,
        'grupo_selecionado': grupo_selecionado,
        'despesas': despesas,
        'despesa_form': despesa_form,
        'participantes_despesa': Divisao(grupo_selecionado).get_pagamentos() if grupo_selecionado else {},
        'pagamento_form': pagamento_form,
    }
    return render(request, template_name='home/sumario.html', context=context, status=200)


def consultas_view(request):

    participante_grupo = ParticipanteGrupo.objects.filter(usuario=request.user)
    print(participante_grupo)    

    return render(request, template_name='home/consultas.html')
