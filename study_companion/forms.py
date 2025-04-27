from django import forms
from .models import Disciplina, Flashcard, Anotacao, EventoCalendario, Receita, Lembrete, AtividadeRelaxamento, MensagemMotivacional
from ckeditor.widgets import CKEditorWidget

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'descricao', 'periodo', 'cor_hex']
        widgets = {
            'cor_hex': forms.TextInput(attrs={'type': 'color'}),
        }

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['pergunta', 'resposta', 'disciplina', 'dificuldade']

class AnotacaoForm(forms.ModelForm):
    class Meta:
        model = Anotacao
        fields = ['titulo', 'disciplina', 'categoria', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título da anotação...'
            }),
            'disciplina': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'conteudo': CKEditorWidget(), 
        }

class EventoCalendarioForm(forms.ModelForm):
    class Meta:
        model = EventoCalendario
        fields = ['titulo', 'data', 'tipo', 'disciplina', 'descricao']
        widgets = {
            'data': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EventoCalendarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.data:
            self.initial['data'] = self.instance.data.strftime('%Y-%m-%dT%H:%M')

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = '__all__'
        widgets = {
            'ingredientes': forms.Textarea(attrs={'rows': 3}),
            'valor_nutricional': forms.Textarea(attrs={'rows': 2}),
        }

class LembreteForm(forms.ModelForm):
    class Meta:
        model = Lembrete
        fields = '__all__'
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
            'intervalo': forms.NumberInput(attrs={'min': 1}),
            'dias_semana': forms.TextInput(attrs={'placeholder': 'Ex: 0111110 (seg a sex)'}),
        }

class AtividadeRelaxamentoForm(forms.ModelForm):
    class Meta:
        model = AtividadeRelaxamento
        fields = ['titulo', 'descricao', 'duracao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Título da atividade'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Descrição...'}),
            'duracao': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Duração em minutos'}),
        }

class MensagemMotivacionalForm(forms.ModelForm):
    class Meta:
        model = MensagemMotivacional
        fields = ['conteudo', 'autor', 'agendada_para']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escreva sua mensagem motivacional...'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Nome do autor'}),
            'agendada_para': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }