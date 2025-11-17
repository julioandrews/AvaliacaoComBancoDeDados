from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg, Count, Max, Min
from django.db import connection
from .models import *

def home(request):
    # Estatísticas para a homepage
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    total_disciplinas = Disciplina.objects.count()
    total_avaliacoes = Avaliacao.objects.count()

    return render(request, 'home.html', {
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'total_disciplinas': total_disciplinas,
        'total_avaliacoes': total_avaliacoes,
    })

# CADASTROS
def cadastrar_aluno(request):
    if request.method == 'POST':
        cpf = request.POST['cpf']
        nome = request.POST['nome']
        turma = request.POST['turma']
        semestre = request.POST['semestre']
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO aluno (cpf, nome, turma, semestre) VALUES (%s,%s,%s,%s)""", [cpf, nome, turma, semestre])
        cursor.close()
        Aluno.objects.create(
            cpf=cpf, nome=nome, turma=turma, semestre=semestre
        )
        return redirect('lista_alunos')
    
    return render(request, 'cadastrar_aluno.html')

def cadastrar_professor(request):
    if request.method == 'POST':
        cpf=request.POST['cpf']
        nome=request.POST['nome']
        data_nasc=request.POST['data_nasc']
        salario=request.POST['salario']        
        idade=request.POST['idade']
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO professor (cpf, nome, data_nasc, salario, idade) VALUES (%s,%s,%s,%s,%s)""", [cpf, nome, data_nasc, salario, idade])
        Professor.objects.create(
            cpf=request.POST['cpf'],
            nome=request.POST['nome'],
            data_nasc=request.POST['data_nasc'],
            salario=request.POST['salario'],
            idade=request.POST['idade']
        )
        return redirect('lista_professores')
    
    return render(request, 'cadastrar_professor.html')

def cadastrar_disciplina(request):
    if request.method == 'POST':
        nome=request.POST['nome']
        descricao=request.POST['descricao']
        professor_cpf=request.POST['professor']
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO disciplina (cpf, nome, descricao) VALUES (%s,%s,%s)""", [professor_cpf, nome, descricao])
        Disciplina.objects.create(
            nome=request.POST['nome'],
            descricao=request.POST['descricao'],
            professor_cpf=request.POST['professor']
        )
        return redirect('lista_disciplinas')
    with connection.cursor() as cursor2:
        cursor2.execute("SELECT * FROM professor")
        professores = cursor2.fetchall()
    return render(request, 'cadastrar_disciplina.html', {'professores': professores})

def cadastrar_questao(request):
    if request.method == 'POST':
        tipo = request.POST['tipo']
        pergunta = request.POST['pergunta']

        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO questao (tipo, pergunta) VALUES (%s,%s)""", [tipo, pergunta])

        questao = Questao.objects.create(tipo=tipo, pergunta=pergunta)
        if tipo == 'OBJETIVA':

            with connection.cursor() as cursor2:
                resposta_certa=request.POST['resposta_certa']
                cursor2.execute("""INSERT INTO q_objetiva (tipo, pergunta, resposta_certa) VALUES (%s,%s,%s)""", [tipo, pergunta, resposta_certa])

            QuestaoObjetiva.objects.create(
                questao_ptr=questao,
                resposta_certa=request.POST['resposta_certa']
            )
            # Cadastrar opções
            for letra in ['A', 'B', 'C', 'D']:
                opcao_texto = request.POST.get(f'opcao_{letra}')
                if opcao_texto:
                    with connection.cursor() as cursor3:
                        cursor3.execute("SELECT* FROM questao")
                        numero = cursor3.fetchall()
                        cod = len(numero)
                        cursor3.execute("""INSERT INTO opcoes (cod, opcao, letra) VALUES (%s,%s,%s)""", [cod, opcao_texto, letra])
                    Opcao.objects.create(
                        questao=questao,
                        letra=letra,
                        opcao_texto=opcao_texto
                    )
        else:
            resposta_esperada=request.POST['resposta_esperada']
            with connection.cursor() as cursor4:
                cursor4.execute("""INSERT INTO q_descritiva (tipo, pergunta, resposta_esperada) VALUES (%s,%s,%s)""", [tipo, pergunta, resposta_esperada])
            QuestaoDescritiva.objects.create(
                questao_ptr=questao,
                resposta_esperada=request.POST['resposta_esperada']
            )
        
        return redirect('lista_questoes')
    
    return render(request, 'cadastrar_questao.html')

def cadastrar_avaliacao(request):
    if request.method == 'POST':
        descricao=request.POST['descricao']
        data=request.POST['data']
        horario=request.POST['horario']
        valor_total=request.POST['valor_total']
        professor_cpf=request.POST['professor']
        disciplina_cod=request.POST['disciplina']
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO avaliacao (descricao, data, horario, valor_total, professor_cpf, disciplina_cod) VALUES (%s,%s,%s,%s,%s,%s)",
                           [descricao, data, horario, valor_total, professor_cpf, disciplina_cod])
        avaliacao = Avaliacao.objects.create(
            descricao=request.POST['descricao'],
            data=request.POST['data'],
            horario=request.POST['horario'],
            valor_total=request.POST['valor_total'],
            professor_id=request.POST['professor'],
            disciplina_id=request.POST['disciplina']
        )
        
        # Adicionar questões
        questao_ids = request.POST.getlist('questoes')
        for questao_id in questao_ids:
            valor = request.POST.get(f'valor_{questao_id}', 1)
            with connection.cursor() as cursor2:
                cursor2.execute("INSERT INTO questoes_usadas (a_cod, q_cod, valor) VALUES (%s, %s, %s)", [avaliacao, questao_id, valor])
            QuestaoUsada.objects.create(
                avaliacao=avaliacao,
                questao_id=questao_id,
                valor=valor
            )
        
        return redirect('lista_avaliacoes')
    
    professores = Professor.objects.all()
    disciplinas = Disciplina.objects.all()
    questões = Questao.objects.all()
    return render(request, 'cadastrar_avaliacao.html', {
        'professores': professores,
        'disciplinas': disciplinas,
        'questoes': questões
    })

# LISTAS
def lista_alunos(request):
    alunos = Aluno.objects.raw("SELECT * FROM myapp_aluno")
    return render(request, 'lista_alunos.html', {'alunos': alunos})

def lista_professores(request):
    professores = Professor.objects.raw("SELECT * FROM myapp_professor")
    return render(request, 'lista_professores.html', {'professores': professores})

def lista_disciplinas(request):
    disciplinas = Disciplina.objects.raw("SELECT * FROM myapp_disciplina")
    return render(request, 'lista_disciplinas.html', {'disciplinas': disciplinas})

def lista_questoes(request):
    questões = Questao.objects.raw("SELECT * FROM myapp_questao")
    return render(request, 'lista_questoes.html', {'questoes': questões})

def lista_avaliacoes(request):
    avaliacoes = Avaliacao.objects.raw("SELECT * FROM myapp_questao")
    return render(request, 'lista_avaliacoes.html', {'avaliacoes': avaliacoes})

# REALIZAR AVALIAÇÃO - MELHORADA
def realizar_avaliacao(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, pk=avaliacao_id)
    questões_usadas = QuestaoUsada.objects.filter(avaliacao=avaliacao)
    
    if request.method == 'POST':
        aluno_cpf = request.POST['aluno_cpf']
        
        # Verificar se aluno existe
        try:
            aluno = Aluno.objects.get(cpf=aluno_cpf)
        except Aluno.DoesNotExist:
            return render(request, 'realizar_avaliacao.html', {
                'avaliacao': avaliacao,
                'questoes': questões_usadas,
                'alunos': Aluno.objects.all(),
                'erro': 'Aluno não encontrado! Verifique o CPF.'
            })
        
        # Verificar se aluno já fez esta prova
        if ProvaFeita.objects.filter(aluno=aluno, avaliacao=avaliacao).exists():
            return render(request, 'realizar_avaliacao.html', {
                'avaliacao': avaliacao,
                'questoes': questões_usadas,
                'alunos': Aluno.objects.all(),
                'erro': 'Aluno já realizou esta avaliação'
            })
        
        # Criar prova com nota 0 inicialmente (será calculada depois)
        prova_feita = ProvaFeita.objects.create(
            aluno=aluno, avaliacao=avaliacao, nota_final=0
        )
        
        # Processar respostas
        for questao_usada in questões_usadas:
            resposta = request.POST.get(f'resposta_{questao_usada.questao.cod}')
            if resposta:
                # Para questões objetivas, a nota será calculada depois
                # Para questões descritivas, nota inicial é 0 (professor corrige depois)
                nota = 0
                if questao_usada.questao.tipo == 'OBJETIVA':
                    # Apenas armazenamos a resposta, a correção será automática
                    nota = 0  # Será calculada na correção
                
                RespostaDada.objects.create(
                    aluno=aluno,
                    avaliacao=avaliacao,
                    questao=questao_usada.questao,
                    resposta=resposta,
                    nota_questao=nota
                )
        
        return redirect('corrigir_prova', prova_id=prova_feita.pk)
    
    return render(request, 'realizar_avaliacao.html', {
        'avaliacao': avaliacao,
        'questoes': questões_usadas,
        'alunos': Aluno.objects.all()
    })

# NOVA FUNCIONALIDADE: CORRIGIR PROVA
def corrigir_prova(request, prova_id):
    prova = get_object_or_404(ProvaFeita, pk=prova_id)
    respostas = RespostaDada.objects.filter(aluno=prova.aluno, avaliacao=prova.avaliacao)
    questões_usadas = QuestaoUsada.objects.filter(avaliacao=prova.avaliacao)
    
    if request.method == 'POST':
        nota_total = 0
        
        for questao_usada in questões_usadas:
            resposta = respostas.filter(questao=questao_usada.questao).first()
            if resposta:
                if questao_usada.questao.tipo == 'OBJETIVA':
                    # Correção automática para questões objetivas
                    try:
                        questao_obj = QuestaoObjetiva.objects.get(pk=questao_usada.questao.cod)
                        if resposta.resposta.upper() == questao_obj.resposta_certa:
                            nota_questao = questao_usada.valor
                        else:
                            nota_questao = 0
                    except QuestaoObjetiva.DoesNotExist:
                        nota_questao = 0
                else:
                    # Para questões descritivas, o professor dá a nota
                    nota_questao = float(request.POST.get(f'nota_{questao_usada.questao.cod}', 0))
                
                # Atualizar nota da questão
                resposta.nota_questao = min(nota_questao, questao_usada.valor)
                resposta.save()
                nota_total += resposta.nota_questao
        
        # Atualizar nota final da prova
        prova.nota_final = nota_total
        prova.save()
        
        return redirect('resultado_avaliacao', prova_id=prova.pk)
    
    return render(request, 'corrigir_prova.html', {
        'prova': prova,
        'respostas': respostas,
        'questoes_usadas': questões_usadas
    })

def resultado_avaliacao(request, prova_id):
    prova = get_object_or_404(ProvaFeita, pk=prova_id)
    respostas = RespostaDada.objects.filter(aluno=prova.aluno, avaliacao=prova.avaliacao)
    
    return render(request, 'resultado_avaliacao.html', {
        'prova': prova,
        'respostas': respostas
    })

# RELATÓRIOS MELHORADOS
def relatorio_aluno(request, aluno_cpf):
    aluno = get_object_or_404(Aluno, cpf=aluno_cpf)
    provas = ProvaFeita.objects.filter(aluno=aluno)
    
    # Estatísticas
    if provas.exists():
        media = provas.aggregate(Avg('nota_final'))['nota_final__avg']
        melhor_nota = provas.aggregate(Max('nota_final'))['nota_final__max']
        pior_nota = provas.aggregate(Min('nota_final'))['nota_final__min']
        total_provas = provas.count()
    else:
        media = melhor_nota = pior_nota = total_provas = 0
    
    return render(request, 'relatorio_aluno.html', {
        'aluno': aluno,
        'provas': provas,
        'media': media,
        'melhor_nota': melhor_nota,
        'pior_nota': pior_nota,
        'total_provas': total_provas
    })

def relatorio_disciplina(request, disciplina_id):
    disciplina = get_object_or_404(Disciplina, pk=disciplina_id)
    avaliacoes = Avaliacao.objects.filter(disciplina=disciplina)
    
    dados_avaliacoes = []
    for avaliacao in avaliacoes:
        provas = ProvaFeita.objects.filter(avaliacao=avaliacao)
        if provas.exists():
            stats = provas.aggregate(
                media=Avg('nota_final'),
                max=Max('nota_final'),
                min=Min('nota_final'),
                count=Count('pk')
            )
            dados_avaliacoes.append({
                'avaliacao': avaliacao,
                'media': stats['media'],
                'max': stats['max'],
                'min': stats['min'],
                'count': stats['count']
            })
    
    return render(request, 'relatorio_disciplina.html', {
        'disciplina': disciplina,
        'dados_avaliacoes': dados_avaliacoes
    })

# NOVO: RELATÓRIO GERAL COM ESTATÍSTICAS
def relatorio_geral(request):
    # Estatísticas gerais
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    total_disciplinas = Disciplina.objects.count()
    total_avaliacoes = Avaliacao.objects.count()
    
    # Top alunos - CORRIGIDO: usando 'pk' em vez de 'id'
    top_alunos = ProvaFeita.objects.values(
        'aluno__nome', 'aluno__cpf'
    ).annotate(
        media=Avg('nota_final'),
        total_provas=Count('pk')
    ).order_by('-media')[:5]
    
    # Disciplinas com melhor desempenho - CORRIGIDO: usando o campo correto
    disciplinas_desempenho = Avaliacao.objects.values(
        'disciplina__nome'
    ).annotate(
        media_geral=Avg('provafeita__nota_final'),
        total_avaliacoes=Count('pk')
    ).filter(media_geral__isnull=False).order_by('-media_geral')
    
    return render(request, 'relatorio_geral.html', {
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'total_disciplinas': total_disciplinas,
        'total_avaliacoes': total_avaliacoes,
        'top_alunos': top_alunos,
        'disciplinas_desempenho': disciplinas_desempenho
    })
