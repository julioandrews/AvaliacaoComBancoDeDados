from django.db import models

class Professor(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100)
    data_nasc = models.DateField(null=True, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    idade = models.IntegerField()

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100)
    turma = models.CharField(max_length=100)
    semestre = models.IntegerField()

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    cod = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Questao(models.Model):
    TIPO_CHOICES = [
        ('OBJETIVA', 'Objetiva'),
        ('DESCRITIVA', 'Descritiva'),
    ]
    
    cod = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    pergunta = models.CharField(max_length=300)

    def __str__(self):
        return f"Questão {self.cod}: {self.pergunta[:50]}..."

class QuestaoObjetiva(Questao):
    resposta_certa = models.CharField(max_length=1)

    class Meta:
        db_table = 'myapp_q_objetiva'

class QuestaoDescritiva(Questao):
    resposta_esperada = models.CharField(max_length=300)

    class Meta:
        db_table = 'myapp_q_descritiva'

class Opcao(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    opcao_texto = models.CharField(max_length=300)
    letra = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.letra}) {self.opcao_texto}"

class Avaliacao(models.Model):
    cod = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=300)
    data = models.DateField()
    horario = models.TimeField()
    valor_total = models.IntegerField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f"Avaliação {self.cod}: {self.descricao}"

class QuestaoUsada(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    valor = models.IntegerField()

    class Meta:
        unique_together = ['avaliacao', 'questao']

class AlunoCursaDisciplina(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['aluno', 'disciplina']

class ProvaFeita(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        unique_together = ['aluno', 'avaliacao']

class RespostaDada(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=300)
    nota_questao = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        unique_together = ['aluno', 'avaliacao', 'questao']
