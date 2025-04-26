from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

PERIODO_CHOICES = [(i, f"{i}° Período") for i in range(1, 13)]

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    periodo = models.IntegerField(choices=PERIODO_CHOICES)
    descricao = models.TextField(blank=True)
    cor_hex = models.CharField(max_length=7, default="#FFFFFF")
    
    def __str__(self):
        return f"{self.nome} ({self.periodo}° período)"
    

class Flashcard(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='flashcard')
    pergunta = models.TextField()
    resposta = models.TextField()
    dificuldade = models.IntegerField(choices=[(1, 'Fácil'), (2, 'Médio'), (3, 'Difícil')])
    ultima_revisao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Flashcard: {self.pergunta[:30]}..."
    
    def marcar_revisado(self):
        self.ultima_revisao = timezone.now()
        self.save()


class Anotacao(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='anotacoes')
    titulo = models.CharField(max_length=200)
    conteudo = RichTextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=50, choices=[
        ('aula', 'Anotação de Aula'),
        ('caso', 'Caso Clínico'),
        ('resumo', 'Resumo'),
    ])

    def __str__(self):
        return f"{self.titulo} ({self.get_categoria_display()})"
    

class EventoCalendario(models.Model):
    titulo =  models.CharField(max_length=100)
    data = models.DateTimeField()
    tipo = models.CharField(max_length=50, choices=[
        ('prova', 'Prova'),
        ('trabalho', 'Trabalho'),
        ('plantao', 'Plantão'),
        ('outro', 'Outro'),
    ])
    disciplina = models.ForeignKey(Disciplina, null=True, blank=True, on_delete=models.SET_NULL, related_name='eventos')
    descricao = models.TextField(blank=True)
    concluido = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.titulo} - {self.data.strftime('%d/%m/%Y %H:%M')}"
    
    @property
    def is_upcoming(self):
        return self.data > timezone.now()
    

class Receita(models.Model):
    nome = models.CharField(max_length=100)
    ingredientes = models.TextField()
    tempo_preparo = models.IntegerField(help_text="Tempo em minutos")
    dificuldade = models.CharField(max_length=50, choices=[
        ('fácil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil'),
    ])
    valor_nutricional = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} ({self.get_dificuldade_display()}) - {self.tempo_preparo} min"


class PlanejamentoRefeicao(models.Model):
    dia_semana = models.IntegerField(choices=[(0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'),
                                              (3, 'Quinta'), (4, 'Sexta'), (5, 'Sábado'), (6, 'Domingo')])
    cafe_manha = models.ForeignKey(Receita, related_name='cafe_manha', blank=True, null=True, on_delete=models.SET_NULL)
    almoco = models.ForeignKey(Receita, related_name='almoco', blank=True, null=True, on_delete=models.SET_NULL)
    jantar = models.ForeignKey(Receita, related_name='jantar', blank=True, null=True, on_delete=models.SET_NULL)
    lanches = models.ForeignKey(Receita, related_name='lanches', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Planejamento de Refeição"
        verbose_name_plural = "Planejamento de Refeições"

    def __str__(self):
        return f"Refeições de {self.get_dia_semana_display()}"


class Lembrete(models.Model):
    tipo = models.CharField(max_length=50, choices=[
        ('pausa', 'Pausa'),
        ('agua', 'Hidratação'),
        ('alongamento', 'Alongamento'),
        ('outro', 'Outro'),
    ])
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    intervalo = models.IntegerField(help_text="Intervalo em minutos")
    dias_semana = models.CharField(max_length=7, help_text="String de 7 caracteres (0/1) para cada dia semana")
    mensagem = models.CharField(max_length=200)

    def __str__(self):
        f"Lembrete {self.get_tipo_display()}: {self.mensagem[:30]}"


class AtividadeRelaxamento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    duracao = models.IntegerField(help_text="Duração em minutos")

    class Meta:
        verbose_name = "Atividade de Relaxamento"
        verbose_name_plural = "Atividades de Relaxamento"

    def __str__(self):
        return f"{self.titulo} ({self.duracao} min)"
    

class MensagemMotivacional(models.Model):
    conteudo = models.TextField()
    autor = models.CharField(max_length=100, default="Você")
    data_criacao = models.DateTimeField(auto_now_add=True)
    agendada_para = models.DateTimeField(null=True, blank=True)
    entregue = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensagem Motivacional"
        verbose_name_plural = "Mensagens Motivacionais"

    def __str__(self):
        return f"Mensagem de {self.autor}: {self.conteudo[:30]}..."
    

class RecadoMural(models.Model):
    conteudo = models.TextField()
    autor = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f"Recado de {self.autor}, {self.conteudo[:30]}..."
    
    def marcar_como_lido(self):
        self.lido = True
        self.save()