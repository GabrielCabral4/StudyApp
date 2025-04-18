from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('disciplinas/', views.disciplinas_list, name='disciplinas'),
    path('disciplinas/nova/', views.disciplina_create, name='disciplina_add'),
    path('disciplinas/<int:pk>/editar', views.disciplina_update, name='disciplina_edit'),
    path('disciplinas/<int:pk>/deletar', views.disciplina_delete, name='disciplina_delete'),
    path('flashcards/', views.flashcards_list, name='flashcards'),
    path('flashcards/nova/', views.flashcard_create, name='flashcard_add'),
    path('flashcards/<int:pk>/editar', views.flashcard_update, name='flashcard_edit'),
    path('flashcards/<int:pk>/deletar', views.flashcard_delete, name='flashcard_delete'),
    path('anotacoes/', views.anotacoes_list, name='anotacoes'),
    path('anotacoes/nova/', views.anotacao_create, name='anotacao_add'),
    path('anotacoes/<int:pk>/editar', views.anotacao_update, name='anotacao_edit'),
    path('anotacoes/<int:pk>/deletar', views.anotacao_delete, name='anotacao_delete'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('refeicoes/', views.refeicoes_list, name='refeicoes'),
    path('receitas/', views.receitas_list, name='receitas'),
    path('lembretes/', views.lembretes_list, name='lembretes'),
    path('relaxamento/', views.relaxamento_list, name='relaxamento'),
    path('motivacional/', views.motivacional_list, name='motivacional'),
    path('mural/', views.mural_view, name='mural'),
    path('settings/', views.settings_view, name='settings'),
    path('account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),
]