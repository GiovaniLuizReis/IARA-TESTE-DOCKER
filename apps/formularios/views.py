from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Formulario, Pergunta, OpcaoPergunta, RegraPulo
from .forms import FormularioForm, PerguntaForm, OpcaoForm, RegraPuloForm
from django.views.decorators.clickjacking import xframe_options_sameorigin

@login_required
def listar_formularios(request):
    formularios = Formulario.objects.all().order_by('parte', 'ordem')
    return render(request, 'listar_formularios.html', {'formularios': formularios, 'active_page': 'formularios'})

@login_required
def cadastrar_formulario(request):
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formulário cadastrado com sucesso.')
            return redirect('listar_formularios')
    else:
        form = FormularioForm()
    return render(request, 'cadastrar_formularios.html', {'form': form, 'active_page': 'formularios'})

@login_required
def editar_formulario(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    if request.method == 'POST':
        form = FormularioForm(request.POST, instance=formulario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formulário atualizado com sucesso.')
            return redirect('listar_formularios')
    else:
        form = FormularioForm(instance=formulario)
    return render(request, 'editar_formularios.html', {'form': form, 'formulario': formulario, 'active_page': 'formularios'})

@login_required
def excluir_formulario(request, formulario_id):
    if request.method == 'POST':
        formulario = get_object_or_404(Formulario, id=formulario_id)
        formulario.delete()
        messages.success(request, 'Formulário removido com sucesso.')
    return redirect('listar_formularios')

@login_required
def gerenciar_estrutura(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    perguntas = formulario.perguntas.all().prefetch_related('opcoes', 'regras_origem')
    return render(request, 'gerenciar_estrutura.html', {'formulario': formulario, 'perguntas': perguntas, 'active_page': 'formularios'})

@login_required
def cadastrar_pergunta(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    if request.method == 'POST':
        form = PerguntaForm(request.POST, request.FILES )
        if form.is_valid():
            pergunta = form.save(commit=False)
            pergunta.formulario = formulario
            pergunta.save()
            messages.success(request, 'Pergunta adicionada com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=formulario.id)
    else:
        form = PerguntaForm()
    return render(request, 'cadastrar_pergunta.html', {'form': form, 'formulario': formulario, 'active_page': 'formularios'})

@login_required
def editar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    if request.method == 'POST':
        form = PerguntaForm(request.POST, request.FILES, instance=pergunta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pergunta atualizada com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=pergunta.formulario.id)
    else:
        form = PerguntaForm(instance=pergunta)
    return render(request, 'editar_pergunta.html', {'form': form, 'pergunta': pergunta, 'active_page': 'formularios'})

@login_required
def excluir_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    formulario_id = pergunta.formulario.id
    if request.method == 'POST':
        pergunta.delete()
        messages.success(request, 'Pergunta removida com sucesso.')
    return redirect('gerenciar_estrutura', formulario_id=formulario_id)

@login_required
def visualizar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    return render(request, 'visualizar_pergunta.html', {'pergunta': pergunta, 'active_page': 'formularios'})

@login_required
def cadastrar_opcao(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    if request.method == 'POST':
        form = OpcaoForm(request.POST)
        if form.is_valid():
            opcao = form.save(commit=False)
            opcao.pergunta = pergunta
            opcao.save()
            messages.success(request, 'Opção adicionada com sucesso.')
            #return redirect('gerenciar_estrutura', formulario_id=pergunta.formulario.id)
            url_base =  reverse('gerenciar_estrutura', kwargs={'formulario_id': pergunta.formulario.id})
            return redirect(f"{url_base}#pergunta-{pergunta.id}")
    
    else:
        form = OpcaoForm()
    return render(request, 'cadastrar_opcao.html', {'form': form, 'pergunta': pergunta, 'active_page': 'formularios'})

@login_required
def editar_opcao(request, opcao_id):
    opcao = get_object_or_404(OpcaoPergunta, id=opcao_id)
    if request.method == 'POST':
        form = OpcaoForm(request.POST, instance=opcao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opção atualizada com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=opcao.pergunta.formulario.id)
    else:
        form = OpcaoForm(instance=opcao)
    return render(request, 'editar_opcao.html', {'form': form, 'opcao': opcao, 'active_page': 'formularios'})

@login_required
def excluir_opcao(request, opcao_id):
    opcao = get_object_or_404(OpcaoPergunta, id=opcao_id)
    formulario_id = opcao.pergunta.formulario.id
    if request.method == 'POST':
        opcao.delete()
        messages.success(request, 'Opção removida com sucesso.')
    return redirect('gerenciar_estrutura', formulario_id=formulario_id)

@login_required
def configurar_regra_pulo(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    
    # Busca todas as regras já cadastradas para esta pergunta
    regras_existentes = RegraPulo.objects.filter(pergunta_origem=pergunta)

    if request.method == 'POST':
        # Passa a pergunta_origem no kwargs como o seu form exige
        form = RegraPuloForm(request.POST, pergunta_origem=pergunta)
        if form.is_valid():
            nova_regra = form.save(commit=False)
            nova_regra.pergunta_origem = pergunta
            nova_regra.save()
            
            # Redireciona para a mesma página para limpar o formulário e 
            # permitir que o usuário adicione a próxima regra (Sim -> 4, Não -> 6, etc.)
            return redirect('configurar_regra_pulo', pergunta_id=pergunta.id)
    else:
        # Formulário vazio para adicionar nova regra
        form = RegraPuloForm(pergunta_origem=pergunta)

    context = {
        'pergunta': pergunta,
        'form': form,
        'regras_existentes': regras_existentes,
    }
    return render(request, 'configurar_regra_pulo.html', context)


@login_required
def excluir_regra_pulo(request, regra_id):
    regra = get_object_or_404(RegraPulo, id=regra_id)
    formulario_id = regra.pergunta_origem.formulario.id
    if request.method == 'POST':
        regra.delete()
        messages.success(request, 'Regra de pulo removida.')
    return redirect('gerenciar_estrutura', formulario_id=formulario_id)

@login_required
@xframe_options_sameorigin
def preview_formulario(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    perguntas = formulario.perguntas.all().prefetch_related('opcoes')
    
    return render(request, 'preview_formulario.html', {
        'formulario': formulario, 
        'perguntas': perguntas, 
        'active_page': 'formularios'
    })