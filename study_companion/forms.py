from django import forms
from .models import Disciplina, Flashcard, Anotacao
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