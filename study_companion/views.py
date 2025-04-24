from django.shortcuts import render, redirect, get_object_or_404    
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (Disciplina, Flashcard, Anotacao, EventoCalendario, PlanejamentoRefeicao, Receita, Lembrete, AtividadeRelaxamento, MensagemMotivacional, RecadoMural)
from datetime import datetime, timedelta
from .forms import DisciplinaForm, FlashcardForm, AnotacaoForm, EventoCalendarioForm
from django.views.decorators.http import require_POST
from django.db.models import Q
from calendar import monthrange


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


def disciplinas_list(request):
    periodo_filtro = request.GET.get('periodo')
    search_filtro = request.GET.get('search')
    disciplinas = Disciplina.objects.all().order_by('periodo', 'nome')
    
    if periodo_filtro:
        disciplinas = disciplinas.filter(periodo=periodo_filtro)
    
    if search_filtro:
        disciplinas = disciplinas.filter(nome__icontains=search_filtro)
    
    return render(request, 'study_companion/disciplinas/list.html', {'disciplinas': disciplinas})


def disciplina_create(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('disciplinas')
    else:
        form = DisciplinaForm()
    return render(request, 'study_companion/disciplinas/create.html', {'form': form})


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


def disciplina_delete(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    if request.method == 'POST':
        disciplina.delete()
        return redirect('disciplinas')
    return render(request, 'study_companion/disciplinas/delete.html', {'disciplina': disciplina})


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


def flashcard_create(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flashcards')
    else:
        form = FlashcardForm()
    return render(request, 'study_companion/flashcards/create.html', {'form': form})


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

@require_POST
def flashcard_delete(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk)
    flashcard.delete()
    return redirect('flashcards')


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


def anotacao_create(request):
    if request.method == 'POST':
        form = AnotacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('anotacoes')
    else:
        form = AnotacaoForm()
    return render(request, 'study_companion/anotacoes/create.html', {'form': form})


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


@require_POST
def anotacao_delete(request, pk):
    anotacao = get_object_or_404(Anotacao, pk=pk)
    anotacao.delete()
    return redirect('anotacoes')


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


def evento_create(request):
    if request.method == 'POST':
        form = EventoCalendarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendario')
    else:
        form = EventoCalendarioForm()

    return render(request, 'study_companion/calendario/create.html', {
        'form': form,
    })

def evento_update(request, pk):
    evento = get_object_or_404(EventoCalendario, pk=pk)
    if request.method == 'POST':
        form = EventoCalendarioForm(request.POST, instance=EventoCalendario)
        if form.is_valid():
            form.save()
            return redirect('calendario')
    else:
        form = EventoCalendarioForm(instance=EventoCalendario)
    return render(request, 'study_companion/calendario/update.html', {'form': form, 'evento': evento})


def evento_delete(request, pk):
    evento = get_object_or_404(EventoCalendario, pk=pk)
    if request.method == 'POST':
        evento.delete()
        return redirect('calendario')
    return render(request, 'study_companion/calendario/delete.html', {'evento': evento})


def evento_concluir(request, pk):
    evento = get_object_or_404(EventoCalendario, pk=pk)
    evento.concluido = True
    evento.save()
    messages.sucess(request, f"Evento '{evento.titulo}' marcado como concluído.")
    return redirect('calendario')


def refeicoes_list(request):
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    planos = []

    for i, dia in enumerate(dias):
        plano, created = PlanejamentoRefeicao.objects.get_or_create(dia_semana=i)
        planos.append(plano)

    return render(request, 'study_companion/refeicoes/list.html', {
        'planos': planos,
        'dias': dias
    })


def receitas_list(request):
    dificuldade = request.GET.get('dificuldade')
    tempo_max = request.GET.get('tempo_max')

    receitas = Receita.objects.all()

    if dificuldade:
        receitas = receitas.filter(dificuldade=dificuldade)

    if tempo_max:
        receitas = receitas.filter(tempo_preparo__lte=int(tempo_max))

    return render(request, 'study_companion/receitas/list.html', {
        'receitas': receitas,
        'dificuldades': [('facil', 'Fácil'), ('medio', 'Médio'), ('dificil', 'Difícil')]
    })

def lembretes_list(request):
    lembretes = Lembrete.objects.all()
    return render(request, 'study_companion/lembretes/list.html', {'lembretes': lembretes})


def relaxamento_list(request):
    atividades = AtividadeRelaxamento.objects.all().order_by('duracao')
    duracao = request.GET.get('duracao', None)

    if duracao:
        atividades = atividades.filter(duracao__lte=int(duracao))

    return render(request, 'study_companion/relaxamento/list.html', {'atividades': atividades})


def motivacional_list(request):
    mensagens = MensagemMotivacional.objects.all().order_by('-data_criacao')
    return render(request, 'study_companion/motivacional/list.html', {'mensagens': mensagens})


def mural_view(request):
    recados = RecadoMural.objects.all().order_by('-data_criacao')

    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')
        autor = request.POST.get('autor', 'Você')

        if conteudo:
            RecadoMural.objects.create(conteudo=conteudo, autor=autor)
            return redirect('mural')
        
    return render(request, 'study_companion/mural/view.html', {'recados': recados})


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


def explore(request):
    return render(request, 'study_companion/explore.html')


def analytics(request):
    return render(request, 'study_companion/analytics.html')


def settings_view(request):
    return render(request, 'study_companion/settings.html')


def account_view(request):
    return render(request, 'study_companion/account.html')


def report(request):
    return render(request, 'study_companion/report.html')


def contact(request):
    return render(request, 'study_companion/study_companion/contact.html')


def logout_view(request):
    return render(request, 'study_companion/logout.html')


def study_companion(request):
    return redirect('home')