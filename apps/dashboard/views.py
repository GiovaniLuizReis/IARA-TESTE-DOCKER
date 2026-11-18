from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.participantes.models import Participante
from apps.formularios.models import Formulario
from apps.atividades.models import Atividade

User = get_user_model()


@login_required
def dashboard_view(request):
    # Captura os parâmetros de filtro da URL
    status_filtro = request.GET.get('status')
    sexo_filtro = request.GET.get('sexo')

    # Querysets base
    atividades = Atividade.objects.all().select_related('participante', 'formulario')
    participantes = Participante.objects.all()

    # Aplicação dos filtros
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

    # 3. Cálculo da Progressão de Fases
    fase_parte1 = 0
    fase_parte2 = 0
    fase_concluido = 0

    participantes_com_atividades = participantes.prefetch_related('atividades__formulario')

    for p in participantes_com_atividades:
        atvs = p.atividades.all()
        if not atvs.exists():
            continue
        
        p1_atvs = [a for a in atvs if a.formulario.parte == 'P1']
        p2_atvs = [a for a in atvs if a.formulario.parte == 'P2']
        
        p1_concluidas = all(a.status == 'concluido' for a in p1_atvs) if p1_atvs else True
        p2_concluidas = all(a.status == 'concluido' for a in p2_atvs) if p2_atvs else True
        
        if p1_concluidas and p2_concluidas:
            fase_concluido += 1
        elif p1_concluidas:
            fase_parte2 += 1
        else:
            fase_parte1 += 1

    # Taxa de Conclusão Global (%)
    taxa_conclusao = round((fase_concluido / total_participantes * 100), 1) if total_participantes > 0 else 0

    # 4. DEMOGRAFIA: Distribuição por Sexo (Ajustado para SEXO_CHOICES do model)
    distribuicao_sexo = {
        'masculino': participantes.filter(sexo='masculino').count(),
        'feminino': participantes.filter(sexo='feminino').count(),
        'intersexo': participantes.filter(sexo='intersexo').count(),
        'nao_informado': participantes.filter(Q(sexo__isnull=True) | Q(sexo='')).count()
    }

    # 5. DEMOGRAFIA: Distribuição por Faixa Etária (Calculada dinamicamente via data_nascimento)
    faixas_etarias = {
        '18_29': 0,
        '30_44': 0,
        '45_59': 0,
        '60_plus': 0,
        'nao_informado': 0
    }

    hoje = date.today()
    for p in participantes:
        if p.data_nascimento:
            idade = hoje.year - p.data_nascimento.year - ((hoje.month, hoje.day) < (p.data_nascimento.month, p.data_nascimento.day))
            if idade < 30:
                faixas_etarias['18_29'] += 1
            elif idade < 45:
                faixas_etarias['30_44'] += 1
            elif idade < 60:
                faixas_etarias['45_59'] += 1
            else:
                faixas_etarias['60_plus'] += 1
        else:
            faixas_etarias['nao_informado'] += 1

    # 6. Últimas interações
    atividades_recentes = atividades.order_by('-atualizado_em')[:10]

    contexto = {
        'total_participantes': total_participantes,
        'total_formularios': total_formularios,
        'total_pesquisadores': total_pesquisadores,
        'atividades_concluidas': atividades_concluidas,
        'taxa_conclusao': taxa_conclusao,
        
        'atividades_em_andamento': atividades_em_andamento,
        'atividades_nao_iniciadas': atividades_nao_iniciadas,
        
        'fase_parte1': fase_parte1,
        'fase_parte2': fase_parte2,
        'fase_concluido': fase_concluido,
        
        'distribuicao_sexo': distribuicao_sexo,
        'faixas_etarias': faixas_etarias,
        
        'atividades_recentes': atividades_recentes,
        'active_page': 'dashboard'
    }

    return render(request, 'dashboard.html', contexto)