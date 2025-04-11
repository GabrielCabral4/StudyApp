from django import forms
from .models import Disciplina, Flashcard

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