from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.db import transaction, IntegrityError 
from django.shortcuts import redirect, render
from django.urls import reverse


from app_divide.forms.despesa_form import DespesaForm
from app_divide.forms.pagamento_form import PagamentoForm
from app_divide.forms.amizades_form import ConvidarForm
from app_divide.models import Grupo, ParticipanteGrupo, Pagamento

from app_divide.models.participacao_despesa import ParticipacaoDespesa
from app_divide.service.gerenciar_sumario import GerenciarSumario
from app_divide.service.services import distribuir_centavos



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
    pagamento_form = None
    convite_form = ConvidarForm()
    gerenciar_sumario = None

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

            gerenciar_sumario = GerenciarSumario(grupo_selecionado)

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
        

    pagamento_form = PagamentoForm(grupo=grupo_selecionado) if grupo_selecionado else None

    #print(f"pagamento_form: {pagamento_form}")

    context = {
        'grupos': grupos,
        'pessoas': pessoas,
        'grupo_selecionado': grupo_selecionado,
        'despesas': despesas,
        'despesa_form': despesa_form,
        'valores_individuais': gerenciar_sumario.calcular_valores_individuais() if gerenciar_sumario is not None else {},
        'pagamento_form': pagamento_form,
        'convite_form': convite_form,
    }
    return render(request, template_name='home/sumario.html', context=context, status=200)


def consultas_view(request):

    participante_grupo = ParticipanteGrupo.objects.filter(usuario=request.user)
    print(participante_grupo)    

    return render(request, template_name='home/consultas.html')



def registrar_pagamento_view(request):
    print(f"Request method: {request.method} em registrar_pagamento_view")
    
    if request.method == 'POST':
        grupo_id = request.POST.get('grupo')
        grupo_selecionado = Grupo.objects.get(pk=grupo_id) if grupo_id else None
        pagamento_form = PagamentoForm(request.POST, grupo=grupo_selecionado)

        if pagamento_form.is_valid():
            try:
                with transaction.atomic():
                    pagamento = pagamento_form.save()
                    messages.success(request, 'Pagamento registrado com sucesso.')
            except IntegrityError as ie:
                messages.error(request, f'Erro ao registrar o pagamento: {ie}')
        else:
            messages.error(request, 'Erro no formulário de pagamento. Verifique os campos e tente novamente.')

    url = f"{reverse('sumario')}?grupo={grupo_selecionado.pk}" if grupo_selecionado else reverse('sumario')
    return redirect(url)




def registrar_despesa_view(request):

    print(f"Request method: {request.method} em registrar_despesa_view")

    grupo_id = request.POST.get('grupo') if request.method == 'POST' else request.GET.get('grupo')

    if request.user.is_authenticated and request.method == 'POST':
        grupo_selecionado = Grupo.objects.get(pk=grupo_id) if grupo_id else None
        
        participante_grupo_logado = None

        if grupo_selecionado is not None:
            despesa_form = DespesaForm(request.POST)

            participante_grupo_logado = ParticipanteGrupo.objects.filter(
                        grupo=grupo_selecionado,
                        usuario=request.user,
                        ativo=True,
                    ).first()

            
    
            if participante_grupo_logado is None:
                messages.error(
                        request, 'Você não pode adicionar despesas a este grupo.')
            elif despesa_form.is_valid():
                try:
                    with transaction.atomic():
    
                        despesa = despesa_form.save(commit=False)
                        despesa.grupo = grupo_selecionado
                        despesa.criador = participante_grupo_logado
                        despesa.save()
                        
                        #Atualizar o registro pagamento relacionado a despesa
                        despesa.despesa_paga.create(
                                pagador=participante_grupo_logado,
                                valor_pago=despesa.valor_total,
                            )

                        participantes_grupo = ParticipanteGrupo.objects.filter(
                                                grupo=grupo_selecionado,
                                                ativo=True,
                                            )

                        cotas = distribuir_centavos(despesa.valor_total, len(participantes_grupo))

                        # Registrar a participação nas despesas
                        for participante_grupo, cota in zip(participantes_grupo, cotas):
                            ParticipacaoDespesa.objects.create(
                                despesa=despesa,
                                participante=participante_grupo,
                                valor_devido=cota,
                            )
                        
                        # calculos_participacao = GerenciarDespesas(despesa, grupo_selecionado, participante_grupo_logado, pessoas)
                        # calculos_participacao.gerar_participacao_despesa()
    
                except IntegrityError as ie:
                    messages.error(request, f'Erro ao adicionar a despesa:{ie}')
                    
                messages.success(request, 'Despesa adicionada com sucesso.')
                url = f"{reverse('sumario')}?grupo={grupo_selecionado.pk}"
                return redirect(url)
            
    return redirect('sumario')
    