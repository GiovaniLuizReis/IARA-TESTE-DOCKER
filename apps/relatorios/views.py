import csv
import statistics
from datetime import date
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from apps.participantes.models import Participante 

def calcular_idade(data_nascimento):
    if not data_nascimento:
        return None
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

def calcular_idade_completa(data_nascimento):
    if not data_nascimento:
        return 'N/I'
    hoje = date.today()
    anos = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    meses = hoje.month - data_nascimento.month
    if hoje.day < data_nascimento.day:
        meses -= 1
    if meses < 0:
        meses += 12
    texto_anos = f"{anos} ano{'s' if anos != 1 else ''}"
    texto_meses = f"{meses} mês" if meses == 1 else f"{meses} meses"
    if meses == 0:
        return texto_anos
    return f"{texto_anos} e {texto_meses}"

@login_required
def painel_relatorios(request):
    return render(request, 'painel_relatorios.html')

@login_required
def exportar_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="dados_anonimizados_iara.csv"'
    
    writer = csv.writer(response, delimiter=';')
    
    writer.writerow(['ID_Interno', 'Código_Identificacao', 'Idade_Exata', 'Situacao_Trabalho', 'Tipo_Vinculo'])
    
    participantes = Participante.objects.all().order_by('id')
    
    for p in participantes:
        writer.writerow([
            p.id, 
            p.identificacao if p.identificacao else 'N/I',
            calcular_idade_completa(p.data_nascimento), 
            p.situacao_trabalho if p.situacao_trabalho else 'N/I',
            p.tipo_vinculo if hasattr(p, 'tipo_vinculo') and p.tipo_vinculo else 'N/I'
        ])
        
    return response

@login_required
def exportar_pdf(request):
    participantes_banco = Participante.objects.all()
    total = participantes_banco.count()
    
    stats_vazio = {'media': '-', 'mediana': '-', 'moda': '-', 'min': '-', 'max': '-'}
    
    def calcular_stats(queryset):
        idades = [calcular_idade(p.data_nascimento) for p in queryset if p.data_nascimento]
        idades = [i for i in idades if i is not None]
        
        if not idades:
            return stats_vazio
        
        return {
            'media': round(statistics.mean(idades), 1),
            'mediana': round(statistics.median(idades), 1),
            'moda': statistics.multimode(idades)[0], 
            'min': min(idades),
            'max': max(idades)
        }
        
    stats_geral = calcular_stats(participantes_banco)

    lista_recentes = list(Participante.objects.all().order_by('-id')[:100])
    for p in lista_recentes:
        p.idade_formatada = calcular_idade_completa(p.data_nascimento)

    context = {
        'data_emissao': timezone.now().strftime('%d/%m/%Y'),
        'gerado_por': request.user.get_full_name() or request.user.email,
        
        'total_participantes': total,
        'taxa_conclusao': 0, 
        'total_em_andamento': 0,
        
        'qtd_masculino': 0,
        'pct_masculino': 0,
        'qtd_feminino': 0,
        'pct_feminino': 0,
        
        'media_idade_geral': stats_geral['media'],
        'mediana_idade_geral': stats_geral['mediana'],
        'moda_idade_geral': stats_geral['moda'],
        'min_idade_geral': stats_geral['min'],
        'max_idade_geral': stats_geral['max'],
        
        'media_idade_masculino': stats_vazio['media'],
        'mediana_idade_masculino': stats_vazio['mediana'],
        'moda_idade_masculino': stats_vazio['moda'],
        'min_idade_masculino': stats_vazio['min'],
        'max_idade_masculino': stats_vazio['max'],
        
        'media_idade_feminino': stats_vazio['media'],
        'mediana_idade_feminino': stats_vazio['mediana'],
        'moda_idade_feminino': stats_vazio['moda'],
        'min_idade_feminino': stats_vazio['min'],
        'max_idade_feminino': stats_vazio['max'],
        
        'participantes': lista_recentes 
    }
    
    return render(request, 'relatorio_pdf_template.html', context)