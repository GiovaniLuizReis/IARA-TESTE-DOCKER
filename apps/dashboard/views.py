from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from apps.coletas.models import SessaoPaciente, Coleta
from apps.pacientes.models import Paciente

User = get_user_model()

@login_required
def dashboard_view(request):
    # Buscamos as sessões, pois elas contêm o vínculo com o paciente e o progresso
    sessoes = SessaoPaciente.objects.all().order_by('-ultima_interacao')
    
    context = {
        'total_entrevistados': Paciente.objects.count(),
        'total_formularios': Coleta.objects.count(),
        'total_pesquisadores': User.objects.filter(is_staff=True).count(),
        'total_sincronizacoes': SessaoPaciente.objects.filter(concluida=True).count(),
        'pacientes_recentes': sessoes, # Passamos o queryset de sessões
        'active_page': 'dashboard'
    }
    return render(request, 'dashboard.html', context)