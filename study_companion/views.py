from django.shortcuts import render, redirect, get_object_or_404    
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (Disciplina, Flashcard, Anotacao, EventoCalendario, PlanejamentoRefeicao, Receita, Lembrete, AtividadeRelaxamento, MensagemMotivacional, RecadoMural, Parceria)
from datetime import datetime
from .forms import DisciplinaForm, FlashcardForm, AnotacaoForm, EventoCalendarioForm, ReceitaForm, LembreteForm, AtividadeRelaxamentoForm, MensagemMotivacionalForm, CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from calendar import monthrange
from django.contrib.auth import login
from django.contrib.auth.models import User

@login_required
def home(request):
    proximos_eventos = EventoCalendario.objects.filter(
        data__gte=datetime.now()
    ).order_by('data')[:5]
    lembretes_ativos = Lembrete.objects.all()[:5]
    recados_nao_lidos = RecadoMural.objects.filter(lido=False).order_by('-data_criacao')
    disciplinas = Disciplina.objects.all()

    context = {
        'proximos_eventos': proximos_eventos,
        'lembretes_ativos': lembretes_ativos,
        'recados_nao_lidos': recados_nao_lidos,
        'disciplinas': disciplinas,
        'hoje': datetime.now()
    }
    return render(request, 'study_companion/home.html', context)

@login_required
def disciplinas_list(request):
    periodo_filtro = request.GET.get('periodo')
    search_filtro = request.GET.get('search')
    disciplinas = Disciplina.objects.all().order_by('periodo', 'nome')
    
    if periodo_filtro:
        disciplinas = disciplinas.filter(periodo=periodo_filtro)
    
    if search_filtro:
        disciplinas = disciplinas.filter(nome__icontains=search_filtro)
    
    return render(request, 'study_companion/disciplinas/list.html', {'disciplinas': disciplinas})

@login_required
def disciplina_create(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('disciplinas')
    else:
        form = DisciplinaForm()
    return render(request, 'study_companion/disciplinas/create.html', {'form': form})

@login_required
def disciplina_update(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)

    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('disciplinas')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'study_companion/disciplinas/update.html', {'form': form, 'disciplina': disciplina})

@login_required
def disciplina_delete(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    if request.method == 'POST':
        disciplina.delete()
        return redirect('disciplinas')
    return render(request, 'study_companion/disciplinas/delete.html', {'disciplina': disciplina})

@login_required
def flashcards_list(request):
    disciplinas = Disciplina.objects.all()
    disciplina_id = request.GET.get('disciplina')
    dificuldade = request.GET.get('dificuldade')

    flashcards = Flashcard.objects.all()

    if disciplina_id:
        flashcards = flashcards.filter(disciplina_id=disciplina_id)
    
    if dificuldade:
        flashcards = flashcards.filter(dificuldade=dificuldade)

    return render(request, 'study_companion/flashcards/list.html', {
        'flashcards': flashcards,
        'disciplinas': disciplinas
    })

@login_required
def flashcard_create(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flashcards')
    else:
        form = FlashcardForm()
    return render(request, 'study_companion/flashcards/create.html', {'form': form})

@login_required
def flashcard_update(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)

    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('flashcards')
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, 'study_companion/flashcards/update.html', {'form': form, 'editar': True})

@login_required
@require_POST
def flashcard_delete(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    flashcard.delete()
    return redirect('flashcards')

@login_required
def anotacoes_list(request):
    disciplinas = Disciplina.objects.all()
    disciplina_id = request.GET.get('disciplina')
    categoria = request.GET.get('categoria')
    q = request.GET.get('q')

    anotacoes = Anotacao.objects.all()

    if disciplina_id:
        anotacoes = anotacoes.filter(disciplina_id=disciplina_id)

    if categoria:
        anotacoes = anotacoes.filter(categoria=categoria)

    if q:
        anotacoes = anotacoes.filter(
         Q(titulo__icontains=q) |
         Q(conteudo__icontains=q)
        )

    return render(request, 'study_companion/anotacoes/list.html', {
        'anotacoes': anotacoes,
        'disciplinas': disciplinas,
        'categorias': [('aula', 'Anotação de Aula'), ('caso', 'Caso Clínico'), ('resumo', 'Resumo')]
    })

@login_required
def anotacao_create(request):
    if request.method == 'POST':
        form = AnotacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('anotacoes')
    else:
        form = AnotacaoForm()
    return render(request, 'study_companion/anotacoes/create.html', {'form': form})

@login_required
def anotacao_update(request, pk):
    anotacao = get_object_or_404(Anotacao, pk=pk)

    if request.method == 'POST':
        form = AnotacaoForm(request.POST, instance=anotacao)
        if form.is_valid():
            form.save()
            return redirect('anotacoes')
    else:
        form = AnotacaoForm(instance=anotacao)
    return render(request, 'study_companion/anotacoes/update.html', {'form': form, 'anotacao': anotacao})

@login_required
@require_POST
def anotacao_delete(request, pk):
    anotacao = get_object_or_404(Anotacao, pk=pk)
    anotacao.delete()
    return redirect('anotacoes')

@login_required
def calendario_view(request):
    hoje = datetime.now()
    mes_atual = hoje.month
    ano_atual = hoje.year

    mes = int(request.GET.get('mes', mes_atual))
    ano = int(request.GET.get('ano', ano_atual))

    proximos_eventos = EventoCalendario.objects.filter(
        data__gte=hoje
    ).order_by('data')

    inicio_mes = datetime(ano, mes, 1)
    _, dias_no_mes = monthrange(ano, mes)
    fim_mes = datetime(ano, mes, dias_no_mes, 23, 59, 59)

    eventos = EventoCalendario.objects.filter(
        data__gte=inicio_mes,
        data__lte=fim_mes
    ).order_by('data')

    dias_grid = []
    for dia in range(1, dias_no_mes + 1):
        data_dia = datetime(ano, mes, dia).date()
        dias_grid.append({'day': dia, 'date': data_dia})

    return render(request, 'study_companion/calendario/view.html', {
        'eventos': eventos,
        'proximos_eventos': proximos_eventos,
        'dias_grid': dias_grid,
        'hoje': hoje,
        'mes_atual': mes,
        'ano_atual': ano,
    })

@login_required
def evento_create(request):
    if request.method == 'POST':
        form = EventoCalendarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendario')
    else:
        form = EventoCalendarioForm()

    return render(request, 'study_companion/calendario/form.html', {
        'form': form,
    })

@login_required
def evento_update(request, pk):
    evento = get_object_or_404(EventoCalendario, pk=pk)
    if request.method == 'POST':
        form = EventoCalendarioForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('calendario')
    else:
        form = EventoCalendarioForm(instance=evento)
    return render(request, 'study_companion/calendario/form.html', {'form': form, 'evento': evento})

@login_required
def evento_delete(request, pk):
    evento = get_object_or_404(EventoCalendario, pk=pk)
    if request.method == 'POST':
        evento.delete()
        return redirect('calendario')
    return render(request, 'study_companion/calendario/delete.html', {'evento': evento})

@login_required
def evento_concluir(request, pk):
    evento = get_object_or_404(EventoCalendario, pk=pk)
    evento.concluido = True
    evento.save()
    messages.sucess(request, f"Evento '{evento.titulo}' marcado como concluído.")
    return redirect('calendario')

@login_required
def refeicoes_list(request):
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    planos = [PlanejamentoRefeicao.objects.get_or_create(dia_semana=i)[0] for i in range(7)]
    receitas = Receita.objects.all()

    if request.method == 'POST':
        for plano in planos:
            cafe_id = request.POST.get(f'cafe_{plano.pk}')
            almoco_id = request.POST.get(f'almoco_{plano.pk}')
            jantar_id = request.POST.get(f'jantar_{plano.pk}')
            lanches_id = request.POST.get(f'lanches_{plano.pk}')

            plano.cafe_manha = Receita.objects.get(id=cafe_id) if cafe_id else None
            plano.almoco = Receita.objects.get(id=almoco_id) if almoco_id else None
            plano.jantar = Receita.objects.get(id=jantar_id) if jantar_id else None
            plano.lanches = Receita.objects.get(id=lanches_id) if lanches_id else None
            plano.save()

        messages.success(request, "Planejamento de refeições atualizado com sucesso!")
        return redirect('refeicoes')

    return render(request, 'study_companion/refeicoes/list.html', {
        'planos': planos,
        'dias': dias,
        'receitas': receitas,
    })

@login_required
def receitas_list(request):
    dificuldade = request.GET.get('dificuldade')
    tempo_max = request.GET.get('tempo_max')
    termo_busca = request.GET.get('search', '')

    receitas = Receita.objects.all()

    if dificuldade:
        receitas = receitas.filter(dificuldade=dificuldade)

    if tempo_max:
        receitas = receitas.filter(tempo_preparo__lte=int(tempo_max))

    if termo_busca:
        receitas = receitas.filter(
            Q(nome__icontains=termo_busca) |
            Q(ingredientes__icontains=termo_busca) |
            Q(valor_nutricional__icontains=termo_busca)
        ).distinct()

    receitas_info = []
    for receita in receitas:
        refeicoes_usadas = list(PlanejamentoRefeicao.objects.filter(
            Q(cafe_manha=receita) |
            Q(almoco=receita) |
            Q(jantar=receita) |
            Q(lanches=receita)
        ).distinct())

        receitas_info.append({
            'receita': receita,
            'refeicoes': refeicoes_usadas
        })

    return render(request, 'study_companion/receitas/list.html', {
        'receitas_info': receitas_info,
        'dificuldades': [('facil', 'Fácil'), ('medio', 'Médio'), ('dificil', 'Difícil')],
        'search': termo_busca
    })

@login_required
def receita_create(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('refeicoes') 
    else:
        form = ReceitaForm()

    return render(request, 'study_companion/receitas/create.html', {'form': form})

@login_required
def receita_update(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    if request.method == 'POST':
        form = ReceitaForm(request.POST, instance=receita)
        if form.is_valid():
            form.save()
            return redirect('receitas')
    else:
        form = ReceitaForm(instance=receita)
    return render(request, 'study_companion/receitas/update.html', {'form': form, 'receita': receita})

@login_required
def receita_delete(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    if request.method == 'POST':
        receita.delete()
        return redirect('receitas')
    return render(request, 'study_companion/receitas/delete.html', {'receita': receita})

@login_required
def lembretes_list(request):
    lembretes = Lembrete.objects.all()
    dias_semana = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"]
    return render(request, 'study_companion/lembretes/list.html', {
        'lembretes': lembretes,
        'dias_semana': dias_semana,
    })

@login_required
def lembrete_create(request):
    if request.method == 'POST':
        form = LembreteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lembretes')
    else:
        form = LembreteForm()
    return render(request, 'study_companion/lembretes/form.html', {'form': form, 'titulo': 'Novo Lembrete'})

@login_required
def lembrete_update(request, pk):
    lembrete = get_object_or_404(Lembrete, pk=pk)
    if request.method == 'POST':
        form = LembreteForm(request.POST, instance=lembrete)
        if form.is_valid():
            form.save()
            return redirect('lembretes')
    else:
        form = LembreteForm(instance=lembrete)
    return render(request, 'study_companion/lembretes/form.html', {'form': form, 'titulo': 'Editar Lembrete'})

@login_required
def lembrete_delete(request, pk):
    lembrete = get_object_or_404(Lembrete, pk=pk)
    if request.method == 'POST':
        lembrete.delete()
        return redirect('lembretes')
    return render(request, 'study_companion/lembretes/delete.html', {'lembrete': lembrete})

@login_required
def relaxamento_list(request):
    atividades = AtividadeRelaxamento.objects.all().order_by('duracao')
    duracao = request.GET.get('duracao', None)

    if duracao:
        atividades = atividades.filter(duracao__lte=int(duracao))

    return render(request, 'study_companion/relaxamento/list.html', {'atividades': atividades})

@login_required
def relaxamento_create(request):
    if request.method == 'POST':
        form = AtividadeRelaxamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade criada com sucesso!')
            return redirect('relaxamento')
    else:
        form = AtividadeRelaxamentoForm()
    return render(request, 'study_companion/relaxamento/create.html', {'form': form})

@login_required
def relaxamento_update(request, pk):
    atividade = get_object_or_404(AtividadeRelaxamento, pk=pk)
    if request.method == 'POST':
        form = AtividadeRelaxamentoForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade atualizada com sucesso!')
            return redirect('relaxamento')
    else:
        form = AtividadeRelaxamentoForm(instance=atividade)
    return render(request, 'study_companion/relaxamento/update.html', {'form': form})

@login_required
def relaxamento_delete(request, pk):
    atividade = get_object_or_404(AtividadeRelaxamento, pk=pk)
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade excluída com sucesso!')
        return redirect('relaxamento')
    return render(request, 'study_companion/relaxamento/delete.html', {'object': atividade})

@login_required
def motivacional_list(request):
    mensagens = MensagemMotivacional.objects.all().order_by('-data_criacao')
    return render(request, 'study_companion/motivacional/list.html', {'mensagens': mensagens})

@login_required
def motivacional_create(request):
    if request.method == 'POST':
        form = MensagemMotivacionalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem criada com sucesso!')
            return redirect('motivacional')
    else:
        form = MensagemMotivacionalForm()
    
    return render(request, 'study_companion/motivacional/form.html', {'form': form, 'modo': 'Adicionar'})

@login_required
def motivacional_update(request, pk):
    mensagem = get_object_or_404(MensagemMotivacional, pk=pk)
    if request.method == 'POST':
        form = MensagemMotivacionalForm(request.POST, instance=mensagem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensagem atualizada com sucesso!')
            return redirect('motivacional')
    else:
        form = MensagemMotivacionalForm(instance=mensagem)
    
    return render(request, 'study_companion/motivacional/form.html', {'form': form, 'modo': 'Editar'})

@login_required
def motivacional_delete(request, pk):
    mensagem = get_object_or_404(MensagemMotivacional, pk=pk)
    
    if request.method == 'POST':
        mensagem.delete()
        messages.success(request, 'Mensagem excluída com sucesso!')
        return redirect('motivacional')
    
    return render(request, 'study_companion/motivacional/delete.html', {'mensagem': mensagem})


@login_required
def mural_view(request):
    user = request.user

    parceria = Parceria.objects.filter(usuario1=user).first() or \
               Parceria.objects.filter(usuario2=user).first()

    if not parceria:
        return render(request, 'study_companion/mural/sem_parceiro.html')

    parceiro = parceria.parceiro_de(user)

    recados = RecadoMural.objects.filter(
        (Q(remetente=user) & Q(destinatario=parceiro)) |
        (Q(remetente=parceiro) & Q(destinatario=user))
    ).order_by('data_criacao')

    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        if conteudo:
            RecadoMural.objects.create(
                conteudo=conteudo,
                remetente=user,
                destinatario=parceiro
            )
            return redirect('mural')

    return render(request, 'study_companion/mural/view.html', {
        'recados': recados,
        'parceiro': parceiro
    })

@login_required
def mural_update(request, pk):
    recado = get_object_or_404(RecadoMural, pk=pk)

    if request.method == 'POST':
        recado.conteudo = request.POST.get('conteudo')
        recado.save()
        messages.success(request, 'Recado atualizado com sucesso!')
        return redirect('mural')
    
    return render(request, 'study_companion/mural/update.html', {'recado': recado})

@login_required
def mural_delete(request, pk):
    recado = get_object_or_404(RecadoMural, pk=pk)

    if request.method == 'POST':
        recado.delete()
        messages.success(request, 'Recado excluído com sucesso!')
        return redirect('mural')
    
    return render(request, 'study_companion/mural/delete.html', {'recado': recado})


@login_required
def gerenciar_parceria(request):
    user = request.user
    parceria_ativa = Parceria.objects.filter(
        (Q(usuario1=user) | Q(usuario2=user)) & Q(aceita=True)
    ).first()

    parceiro = None
    if parceria_ativa:
        parceiro = (
            parceria_ativa.usuario2
            if parceria_ativa.usuario1 == user
            else parceria_ativa.usuario1
        )

    convites_recebidos = Parceria.objects.filter(usuario2=user, aceita=False)
    convites_enviados = Parceria.objects.filter(usuario1=user, aceita=False)

    context = {
        'parceria': parceria_ativa,
        'parceiro': parceiro,
        'convites_recebidos': convites_recebidos,
        'convites_enviados': convites_enviados,
    }
    return render(request, 'study_companion/parcerias/gerenciar.html', context)


@login_required
def enviar_convite_parceria(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            destino = User.objects.get(username=username)
            if destino == request.user:
                messages.error(request, "Você não pode enviar convite para si mesmo.")
            elif Parceria.objects.filter(
                Q(usuario1=request.user, usuario2=destino) | 
                Q(usuario1=destino, usuario2=request.user)
            ).exists():
                messages.error(request, "Já existe uma parceria ou convite com este usuário.")
            else:
                Parceria.objects.create(usuario1=request.user, usuario2=destino)
                messages.success(request, "Convite enviado com sucesso!")
        except User.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
        return redirect('gerenciar_parceria')


@login_required
def aceitar_parceria(request, parceria_id):
    parceria = get_object_or_404(Parceria, id=parceria_id, usuario2=request.user)
    parceria.aceita = True
    parceria.save()
    messages.success(request, "Parceria aceita!")
    return redirect('gerenciar_parceria')


@login_required
def recusar_parceria(request, parceria_id):
    parceria = get_object_or_404(Parceria, id=parceria_id, usuario2=request.user)
    parceria.delete()
    messages.success(request, "Convite recusado.")
    return redirect('gerenciar_parceria')


@login_required
def encerrar_parceria(request, parceria_id):
    parceria = get_object_or_404(Parceria, id=parceria_id)
    if parceria.envolve(request.user):
        parceria.delete()
        messages.success(request, "Parceria encerrada.")
    return redirect('gerenciar_parceria')

@login_required
def dashboard(request):
    disciplinas_count = Disciplina.objects.count()
    flashcards_count = Flashcard.objects.count()
    eventos_proximos_count = EventoCalendario.objects.filter(data__gte=datetime.now().count())

    context = {
        'disciplinas_count': disciplinas_count,
        'flashcards_count': flashcards_count,
        'eventos_proximos_count': eventos_proximos_count
    }

    return render(request, 'study_companion/dashboard.html', context)


def settings_view(request):
    return render(request, 'study_companion/settings.html')

@login_required
def account_view(request):
    return render(request, 'study_companion/account.html')


def logout_view(request):
    return render(request, 'study_companion/logout.html')

@login_required
def perfil_view(request):
    return render(request, 'perfil.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'study_companion/registration/register.html', {'form': form})