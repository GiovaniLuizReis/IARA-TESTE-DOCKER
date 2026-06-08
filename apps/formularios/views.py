import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Formulario, Bloco, Pergunta, OpcaoPergunta, SessaoPaciente, Resposta, RegraPulo
from .forms import FormularioForm, BlocoForm, PerguntaForm, OpcaoForm, RegraPuloForm


# =====================================================================
# GESTÃO DE FORMULÁRIOS (CRUD PRINCIPAL)
# =====================================================================

@login_required
def listar_formularios(request):
    formularios = Formulario.objects.all().order_by('-criado_em')
    return render(
        request,
        'listar_formularios.html',
        {
            'formularios': formularios,
            'active_page': 'formularios'
        }
    )


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

    return render(
        request,
        'cadastrar_formularios.html',
        {
            'form': form,
            'active_page': 'formularios'
        }
    )


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

    return render(
        request,
        'editar_formularios.html',
        {
            'form': form,
            'formulario': formulario,
            'active_page': 'formularios'
        }
    )


@login_required
def excluir_formulario(request, formulario_id):
    if request.method == 'POST':
        formulario = get_object_or_404(Formulario, id=formulario_id)
        formulario.delete()
        messages.success(request, 'Formulário removido com sucesso.')
    return redirect('listar_formularios')


# =====================================================================
# PAINEL DE CONSTRUÇÃO E ESTRUTURA DINÂMICA
# =====================================================================

@login_required
def gerenciar_estrutura(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    blocos = formulario.blocos.all().prefetch_related(
        'perguntas__opcoes', 
        'perguntas__regras_origem'
    )
    return render(
        request,
        'gerenciar_estrutura.html',
        {
            'formulario': formulario,
            'blocos': blocos,
            'active_page': 'formularios'
        }
    )


# =====================================================================
# GERENCIAMENTO DE BLOCOS
# =====================================================================

@login_required
def cadastrar_bloco(request, formulario_id):
    formulario = get_object_or_404(Formulario, id=formulario_id)
    if request.method == 'POST':
        form = BlocoForm(request.POST)
        if form.is_valid():
            bloco = form.save(commit=False)
            bloco.formulario = formulario
            bloco.save()
            messages.success(request, 'Bloco adicionado com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=formulario.id)
    else:
        form = BlocoForm()

    return render(
        request,
        'cadastrar_bloco.html',
        {
            'form': form,
            'formulario': formulario,
            'active_page': 'formularios'
        }
    )


@login_required
def editar_bloco(request, bloco_id):
    bloco = get_object_or_404(Bloco, id=bloco_id)
    if request.method == 'POST':
        form = BlocoForm(request.POST, instance=bloco)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bloco atualizado com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=bloco.formulario.id)
    else:
        form = BlocoForm(instance=bloco)

    return render(
        request,
        'editar_bloco.html',
        {
            'form': form,
            'bloco': bloco,
            'active_page': 'formularios'
        }
    )


@login_required
def excluir_bloco(request, bloco_id):
    bloco = get_object_or_404(Bloco, id=bloco_id)
    formulario_id = bloco.formulario.id
    if request.method == 'POST':
        bloco.delete()
        messages.success(request, 'Bloco removido com sucesso.')
    return redirect('gerenciar_estrutura', formulario_id=formulario_id)


# =====================================================================
# GERENCIAMENTO DE PERGUNTAS
# =====================================================================

@login_required
def cadastrar_pergunta(request, bloco_id):
    bloco = get_object_or_404(Bloco, id=bloco_id)
    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            pergunta = form.save(commit=False)
            pergunta.bloco = bloco
            pergunta.save()
            messages.success(request, 'Pergunta adicionada com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=bloco.formulario.id)
    else:
        form = PerguntaForm()

    return render(
        request,
        'cadastrar_pergunta.html',
        {
            'form': form,
            'bloco': bloco,
            'active_page': 'formularios'
        }
    )


@login_required
def editar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    if request.method == 'POST':
        form = PerguntaForm(request.POST, instance=pergunta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pergunta atualizada com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=pergunta.bloco.formulario.id)
    else:
        form = PerguntaForm(instance=pergunta)

    return render(
        request,
        'editar_pergunta.html',
        {
            'form': form,
            'pergunta': pergunta,
            'active_page': 'formularios'
        }
    )


@login_required
def excluir_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    formulario_id = pergunta.bloco.formulario.id
    if request.method == 'POST':
        pergunta.delete()
        messages.success(request, 'Pergunta removida com sucesso.')
    return redirect('gerenciar_estrutura', formulario_id=formulario_id)


@login_required
def visualizar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    return render(
        request,
        'visualizar_pergunta.html',
        {
            'pergunta': pergunta,
            'active_page': 'formularios'
        }
    )


# =====================================================================
# GERENCIAMENTO DE OPÇÕES DE RESPOSTA
# =====================================================================

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
            return redirect('gerenciar_estrutura', formulario_id=pergunta.bloco.formulario.id)
    else:
        form = OpcaoForm()

    return render(
        request,
        'cadastrar_opcao.html',
        {
            'form': form,
            'pergunta': pergunta,
            'active_page': 'formularios'
        }
    )


@login_required
def editar_opcao(request, opcao_id):
    opcao = get_object_or_404(OpcaoPergunta, id=opcao_id)
    if request.method == 'POST':
        form = OpcaoForm(request.POST, instance=opcao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opção atualizada com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=opcao.pergunta.bloco.formulario.id)
    else:
        form = OpcaoForm(instance=opcao)

    return render(
        request,
        'editar_opcao.html',
        {
            'form': form,
            'opcao': opcao,
            'active_page': 'formularios'
        }
    )


@login_required
def excluir_opcao(request, opcao_id):
    opcao = get_object_or_404(OpcaoPergunta, id=opcao_id)
    formulario_id = opcao.pergunta.bloco.formulario.id
    if request.method == 'POST':
        opcao.delete()
        messages.success(request, 'Opção removida com sucesso.')
    return redirect('gerenciar_estrutura', formulario_id=formulario_id)


# =====================================================================
# GESTÃO DE REGRAS DE PULO (LÓGICA CONDICIONAL)
# =====================================================================

@login_required
def configurar_regra_pulo(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    if request.method == 'POST':
        form = RegraPuloForm(request.POST, pergunta_origem=pergunta)
        if form.is_valid():
            regra = form.save(commit=False)
            regra.pergunta_origem = pergunta
            regra.save()
            messages.success(request, 'Regra de pulo configurada com sucesso.')
            return redirect('gerenciar_estrutura', formulario_id=pergunta.bloco.formulario.id)
    else:
        form = RegraPuloForm(pergunta_origem=pergunta)

    return render(
        request,
        'configurar_regra_pulo.html',
        {
            'form': form,
            'pergunta': pergunta,
            'active_page': 'formularios'
        }
    )


@login_required
def excluir_regra_pulo(request, regra_id):
    regra = get_object_or_404(RegraPulo, id=regra_id)
    formulario_id = regra.pergunta_origem.bloco.formulario.id
    if request.method == 'POST':
        regra.delete()
        messages.success(request, 'Regra de pulo removida com sucesso.')
    return redirect('gerenciar_estrutura', formulario_id=formulario_id)


# =====================================================================
# MOTOR DE RENDEREZAMENTO E CAPTURA (FLUXO DO PACIENTE)
# =====================================================================

def responder_formulario_token(request, token):
    sessao = get_object_or_404(SessaoPaciente, token_acesso=token)
    
    if sessao.concluida:
        return redirect('resposta_sucesso', token=token)
        
    formulario = sessao.coleta.formulario
    
    if not sessao.iniciada_em:
        sessao.iniciada_em = timezone.now()
        sessao.save()

    if not sessao.bloco_atual:
        bloco_atual = formulario.blocos.order_by('ordem').first()
        sessao.bloco_atual = bloco_atual
        sessao.save()
    else:
        bloco_atual = sessao.bloco_atual

    if not bloco_atual:
        messages.error(request, 'Este formulário não possui blocos estruturados.')
        return render(request, 'responder_bloco.html', {'formulario': formulario, 'erro': True})

    perguntas = bloco_atual.perguntas.all().prefetch_related('opcoes')

    if request.method == 'POST':
        erros = []
        respostas_a_salvar = []

        for pergunta in perguntas:
            campo_nome = f'pergunta_{pergunta.id}'
            
            if pergunta.tipo == 'checkbox':
                valores_selecionados = request.POST.getlist(campo_nome)
                if pergunta.obrigatoria and not valores_selecionados:
                    erros.append(f'A pergunta "{pergunta.titulo}" é obrigatória.')
                else:
                    respostas_a_salvar.append((pergunta, valores_selecionados, 'multipla'))
            elif pergunta.tipo == 'matrix':
                opcoes_matriz = pergunta.opcoes.all()
                valores_matriz = {}
                for opcao in opcoes_matriz:
                    chave_sub = f'pergunta_{pergunta.id}_linha_{opcao.id}'
                    val_sub = request.POST.get(chave_sub)
                    if val_sub:
                        valores_matriz[opcao.id] = val_sub
                
                if pergunta.obrigatoria and len(valores_matriz) < opcoes_matriz.count():
                    erros.append(f'Preencha todas as linhas da matriz para a pergunta "{pergunta.titulo}".')
                else:
                    respostas_a_salvar.append((pergunta, valores_matriz, 'matriz'))
            else:
                valor = request.POST.get(campo_nome)
                if pergunta.obrigatoria and not valor:
                    erros.append(f'A pergunta "{pergunta.titulo}" é obrigatória.')
                else:
                    respostas_a_salvar.append((pergunta, valor, 'simples'))

        if erros:
            for erro in erros:
                messages.error(request, erro)
        else:
            for pergunta, dado, tipo_resp in respostas_a_salvar:
                resposta_obj, _ = Resposta.objects.get_or_create(sessao=sessao, pergunta=pergunta)
                
                if tipo_resp == 'multipla':
                    resposta_obj.opcoes_selecionadas.set(OpcaoPergunta.objects.filter(id__in=dado))
                    resposta_obj.valor_texto = ", ".join(dado)
                elif tipo_resp == 'matriz':
                    resposta_obj.valor_texto = json.dumps(dado)
                else:
                    resposta_obj.valor_texto = dado
                    if pergunta.tipo in ['radio', 'select']:
                        opcao_sel = OpcaoPergunta.objects.filter(id=dado).first()
                        if opcao_sel:
                            resposta_obj.opcoes_selecionadas.set([opcao_sel])
                
                resposta_obj.save()

            proximo_bloco = None
            pulo_executado = False
            
            for pergunta in perguntas:
                regras = RegraPulo.objects.filter(pergunta_origem=pergunta)
                for regra in regras:
                    resp_atual = Resposta.objects.filter(sessao=sessao, pergunta=pergunta).first()
                    if resp_atual:
                        if regra.opcao_condicao in resp_atual.opcoes_selecionadas.all() or resp_atual.valor_texto == str(regra.opcao_condicao.id):
                            proximo_bloco = regra.pergunta_destino.bloco
                            pulo_executado = True
                            break
                if pulo_executado:
                    break

            if not pulo_executado:
                proximo_bloco = formulario.blocos.filter(ordem__gt=bloco_atual.ordem).order_by('ordem').first()

            if proximo_bloco:
                sessao.bloco_atual = proximo_bloco
                sessao.save()
                return redirect('responder_formulario_token', token=token)
            else:
                sessao.concluida = True
                sessao.bloco_atual = None
                sessao.save()
                return redirect('resposta_sucesso', token=token)

    return render(
        request, 
        'responder_bloco.html', 
        {
            'formulario': formulario,
            'bloco': bloco_atual,
            'perguntas': perguntas,
            'sessao': sessao
        }
    )


def resposta_sucesso(request, token):
    return render(request, 'resposta_sucesso.html')