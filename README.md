# IARA-SAÚDE

Sistema de Gestão Epidemiológica para acompanhamento de pacientes, aplicação de formulários clínicos e gerenciamento de pesquisa multicêntrica.

## 📌 Objetivo do Sistema

O **IARA-SAÚDE** é uma plataforma desenvolvida para gerenciar o fluxo de pacientes em estudos epidemiológicos e clínicos, permitindo:

- Cadastro e acompanhamento de pacientes;
- Aplicação de questionários em múltiplas etapas;
- Controle de progresso dos formulários;
- Registro de pesquisadores e atendentes responsáveis;
- Auditoria completa de alterações;
- Controle de acesso por centro e estado;
- Registro de exames e atividades do paciente.

---

# 🚀 Fluxo do Sistema

## 1. Cadastro Inicial do Paciente

O **Atendente** entra em contato com o paciente e realiza o cadastro no sistema com informações básicas:

### Dados iniciais do paciente
- Nome completo
- CPF
- E-mail
- Número de inscrição
- Telefone
- Estado
- Centro de pesquisa
- Dados complementares

Após o cadastro:

✅ O paciente é registrado no sistema.

✅ O sistema registra **quem realizou o cadastro**.

✅ Um **link exclusivo é enviado por e-mail** ao paciente.

---

## 2. Resposta do Questionário – Parte 1 (Remota)

O paciente recebe:

- Link individual do formulário
- Número de inscrição

### Características da Parte 1

A Parte 1 do questionário:

- É respondida **em casa**;
- Não exige login no sistema;
- Pode ser respondida a qualquer momento;
- É dividida em **blocos**;
- Cada bloco informa o **tempo estimado de resposta**;
- Possui **salvamento automático de progresso**.

### Requisitos funcionais

O paciente deve poder:

- Iniciar o formulário;
- Parar em qualquer momento;
- Continuar posteriormente do ponto onde parou.

Exemplo:

Parte 1 possui 4 blocos.

Paciente respondeu apenas:

- Bloco 1
- Bloco 2
- Bloco 3

O sistema salva automaticamente e permite continuar depois.

---

## 3. Monitoramento do Progresso

O sistema possui uma tela para acompanhamento dos pacientes.

A equipe poderá visualizar:

- Nome do paciente
- Status do formulário
- Bloco atual
- Se concluiu a Parte 1
- Pendências

### Exemplos de status

- Não iniciado
- Em andamento
- Parte 1 concluída
- Parte 2 concluída
- Finalizado

---

## 4. Atendimento Presencial – Parte 2

Após concluir a Parte 1:

O **Atendente** entra em contato com o paciente para atendimento presencial.

### Fluxo do Pesquisador

No atendimento presencial:

O **Pesquisador** busca o paciente pelo:

- Nome
- Número de inscrição
- Últimos 3 dígitos do CPF

Ao localizar:

➡️ Seleciona **"Responder Questionário – Parte 2"**

O pesquisador responde junto com o paciente.

### Registro obrigatório

O sistema registra:

- Quem auxiliou o paciente;
- Data e hora;
- Alterações realizadas;
- Conclusão da Parte 2.

---

## 5. Recuperação de Questionário Incompleto

Caso o paciente não finalize a Parte 1:

Exemplo:

Paciente respondeu apenas 3 de 4 blocos.

O pesquisador poderá:

- Chamar o paciente presencialmente;
- Continuar a Parte 1 junto com ele;
- Finalizar os blocos pendentes.

### Auditoria

Todas as ações devem registrar:

- Usuário responsável;
- Data;
- Hora;
- Alteração realizada.

---

# 🔐 Controle de Permissões

O sistema terá três níveis de acesso.

## Atendente

Responsável por:

- Cadastro do paciente;
- Acompanhamento do progresso;
- Contato com pacientes;
- Agendamento do presencial.

### Não pode:
- Alterar respostas do formulário.

---

## Pesquisador

Responsável por:

- Buscar paciente;
- Aplicar Parte 2;
- Auxiliar presencialmente;
- Completar Parte 1 se necessário;
- Registrar exames e atividades.

### Pode:
- Alterar respostas do formulário.

### Toda alteração:
Deve ficar registrada no histórico.

---

## Administrador Central

Responsável por:

- Gerenciar centro de pesquisa;
- Criar usuários;
- Cadastrar pesquisadores;
- Cadastrar atendentes;
- Configurar permissões.

---

# 🏥 Controle Multicentro

O sistema é segregado por:

- Centro
- Estado

### Regra de acesso

Usuários de:

**Centro X / Estado X**

❌ Não podem visualizar pacientes do:

**Centro Y / Estado Y**

A visualização dos dados é restrita por vínculo institucional.

---

# 📝 Estrutura do Questionário

O questionário será dividido em:

## Parte 1
Resposta remota pelo paciente.

### Características:
- Em blocos
- Tempo estimado por bloco
- Pode pausar
- Salvamento automático

## Parte 2
Resposta presencial com pesquisador.

---

# 📋 Registro de Exames e Atividades

O sistema permitirá registrar:

### Exames
- Nome do exame
- Data de início
- Data de término
- Observações

### Atividades
- Nome da atividade
- Responsável
- Data de início
- Data de término
- Status

---

# 📜 Auditoria e Histórico

Todas as ações no sistema devem ser auditáveis.

O histórico deve registrar:

- Quem realizou ação
- O que foi alterado
- Quando foi alterado
- Valores antigos e novos

Exemplo:

```txt
Pesquisador João alterou pergunta 12
Resposta anterior: Não
Nova resposta: Sim
Data: 25/05/2026 - 14:30