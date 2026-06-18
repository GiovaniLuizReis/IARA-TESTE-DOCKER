from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Importando os novos modelos baseados na refatoração
from apps.participantes.models import Participante
from apps.formularios.models import Formulario
from apps.atividades.models import Atividade

User = get_user_model()

from django.db.models import Count, Q

@login_required
def dashboard_view(request):
    # Captura os parâmetros de filtro da URL
    status_filtro = request.GET.get('status')
    sexo_filtro = request.GET.get('sexo')

    # Querysets base
    atividades = Atividade.objects.all().select_related('participante', 'formulario')
    participantes = Participante.objects.all()

    # Aplicação dos filtros (se o usuário selecionou algo no menu suspenso)
    if status_filtro:
        atividades = atividades.filter(status=status_filtro)
    if sexo_filtro:
        atividades = atividades.filter(participante__sexo=sexo_filtro)
        participantes = participantes.filter(sexo=sexo_filtro)

    # 1. Métricas para os Cards Principais
    total_participantes = participantes.count()
    total_formularios = Formulario.objects.filter(ativo=True).count()
    total_pesquisadores = User.objects.filter(is_staff=True).count()
    atividades_concluidas = atividades.filter(status='concluido').count()

    # 2. Métricas para o Gráfico de Status (Progresso Geral)
    atividades_em_andamento = atividades.filter(status='em_andamento').count()
    atividades_nao_iniciadas = atividades.filter(status='nao_iniciado').count()

    # 3. CÁLCULO DA PROGRESSÃO DE FASES (Para o gráfico de barras)
    fase_parte1 = 0
    fase_parte2 = 0
    fase_concluido = 0

    # Carrega os participantes e suas atividades para evitar consultas repetitivas no banco (otimização)
    participantes_com_atividades = participantes.prefetch_related('atividades__formulario')

    for p in participantes_com_atividades:
        atvs = p.atividades.all()
        
        # Se o participante não tem atividades, ignoramos no fluxo
        if not atvs.exists():
            continue
        
        # Separa as atividades por parte
        p1_atvs = [a for a in atvs if a.formulario.parte == 'P1']
        p2_atvs = [a for a in atvs if a.formulario.parte == 'P2']
        
        # Verifica se todas as atividades de cada parte estão concluídas
        p1_concluidas = all(a.status == 'concluido' for a in p1_atvs) if p1_atvs else True
        p2_concluidas = all(a.status == 'concluido' for a in p2_atvs) if p2_atvs else True
        
        # Classifica o participante na fase correta
        if p1_concluidas and p2_concluidas:
            fase_concluido += 1
        elif p1_concluidas:
            fase_parte2 += 1
        else:
            fase_parte1 += 1

    # 4. Últimas atividades atualizadas para a tabela
    atividades_recentes = atividades.order_by('-atualizado_em')[:10]

    contexto = {
        # Cards
        'total_participantes': total_participantes,
        'total_formularios': total_formularios,
        'total_pesquisadores': total_pesquisadores,
        'atividades_concluidas': atividades_concluidas,
        
        # Gráfico Status
        'atividades_em_andamento': atividades_em_andamento,
        'atividades_nao_iniciadas': atividades_nao_iniciadas,
        
        # Gráfico Fases
        'fase_parte1': fase_parte1,
        'fase_parte2': fase_parte2,
        'fase_concluido': fase_concluido,
        
        # Tabela
        'atividades_recentes': atividades_recentes,
        'active_page': 'dashboard'
    }

    return render(request, 'dashboard.html', contexto)