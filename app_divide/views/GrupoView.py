from django.utils import timezone

from django.shortcuts import render, redirect
from app_divide.models.grupo import Grupo
from app_divide.models.participante_grupo import ParticipanteGrupo


def criar_grupo(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            nome_grupo = request.POST.get('nome_grupo')
            descricao_grupo = request.POST.get('descricao_grupo')

            print(f"Nome do grupo: {nome_grupo}")
            print(f"Descrição do grupo: {descricao_grupo}")

            if nome_grupo:
                data_criacao = timezone.now()
                grupo = Grupo.objects.create(nome=nome_grupo,
                        descricao=descricao_grupo, data_criacao=data_criacao,
                        criado_por=request.user)
                grupo.save()

                participante = ParticipanteGrupo.objects.create(
                    grupo=grupo,
                    usuario=request.user,
                    ativo=True
                )
                participante.save()
                
            else:
                # Handle the case where the group name is not provided
                return render(request, 'grupo/criar_grupo.html', {'error': 'O nome do grupo é obrigatório.'})

    return redirect('sumario')
    