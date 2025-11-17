from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Cadastros
    path('aluno/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('professor/cadastrar/', views.cadastrar_professor, name='cadastrar_professor'),
    path('disciplina/cadastrar/', views.cadastrar_disciplina, name='cadastrar_disciplina'),
    path('questao/cadastrar/', views.cadastrar_questao, name='cadastrar_questao'),
    path('avaliacao/cadastrar/', views.cadastrar_avaliacao, name='cadastrar_avaliacao'),
    
    # Listas
    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('professores/', views.lista_professores, name='lista_professores'),
    path('disciplinas/', views.lista_disciplinas, name='lista_disciplinas'),
    path('questoes/', views.lista_questoes, name='lista_questoes'),
    path('avaliacoes/', views.lista_avaliacoes, name='lista_avaliacoes'),
    
    # Avaliações
   #path('avaliacao/<int:avaliacao_id>/realizar/', views.realizar_avaliacao, name='realizar_avaliacao'),
   #path('prova/<int:prova_id>/corrigir/', views.corrigir_prova, name='corrigir_prova'),
   #path('resultado/<int:prova_id>/', views.resultado_avaliacao, name='resultado_avaliacao'),
    
    # Relatórios
   #path('relatorio/aluno/<str:aluno_cpf>/', views.relatorio_aluno, name='relatorio_aluno'),
   #path('relatorio/disciplina/<int:disciplina_id>/', views.relatorio_disciplina, name='relatorio_disciplina'),
   #path('relatorio/geral/', views.relatorio_geral, name='relatorio_geral'),
]
