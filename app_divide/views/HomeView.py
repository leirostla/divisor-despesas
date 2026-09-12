from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse

from app_divide.forms.despesa_form import DespesaForm
from app_divide.models import Grupo, ParticipanteGrupo, Pagamento

from app_divide.models.participacao_despesa import ParticipacaoDespesa
from app_divide.service.divisao import Divisao, calcular_divisao


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
        print(f"Grupo selecionado: {grupo_id}")

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
                despesa = despesa_form.save(commit=False)
                despesa.grupo = grupo_selecionado
                despesa.criador = participante
                despesa.save()

                valor_devido = despesa.valor_total / (len(pessoas) + 1)

                participacao_despesa = ParticipacaoDespesa()
                participacao_despesa.despesa = despesa
                participacao_despesa.participante = participante
                participacao_despesa.valor_devido = valor_devido
                participacao_despesa.save()

                for p in pessoas:
                    participacao_despesa = ParticipacaoDespesa()
                    participacao_despesa.despesa = despesa
                    participacao_despesa.participante = ParticipanteGrupo.objects.filter(
                        grupo=grupo_selecionado,
                        usuario=p,
                        ativo=True,
                    ).first()
                    participacao_despesa.valor_devido = valor_devido
                    participacao_despesa.save()

                pagamento_despesa = Pagamento()
                pagamento_despesa.despesa = despesa
                pagamento_despesa.pagador = participante
                pagamento_despesa.valor_pago = despesa.valor_total
                pagamento_despesa.save()

                #divisao = Divisao(grupo_selecionado)

                messages.success(request, 'Despesa adicionada com sucesso.')
                url = f"{reverse('sumario')}?grupo={grupo_selecionado.pk}"
                return redirect(url)

    context = {
        'grupos': grupos,
        'pessoas': pessoas,
        'grupo_selecionado': grupo_selecionado,
        'despesas': despesas,
        'despesa_form': despesa_form,
        'pagamentos': Divisao(grupo_selecionado).get_pagamentos() if grupo_selecionado else {},
    }
    return render(request, template_name='home/sumario.html', context=context, status=200)


def consultas_view(request):

    participante_grupo = ParticipanteGrupo.objects.filter(usuario=request.user)
    print(participante_grupo)    

    return render(request, template_name='home/consultas.html')
