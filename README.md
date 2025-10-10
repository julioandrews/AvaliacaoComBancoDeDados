Essa é uma modelagem de um sistema de avaliações de estudantes em uma universidade.

<h1>Objetivos:</h1>

- Cadastro de provas, com suas informações (horário, valor, e.c.), que usam de diversas questões disponíveis,
- Cadastro de questões, com suas informações (pergunta, resposta, e.c), que podem ser usadas por diversas provas,
- Cadastro de alunos, com suas informações (CPF, curso, e.c.), que podem realizar as provas disponíveis pelas disciplinas que participam,
- Cadastro de disciplinas, com suas informações (nome, descrição, e.c.), que são ministradas por um professor e ofertadas a diversos alunos, e
- Cadastro de professores, com suas informações (CPF, disciplina, e.c.), que ministram disciplinas e aplicam provas.

<h1>Complicações:</h1>

1. É importante que em uma avaliação específica (que se utiliza de questões específicas), cada questão possua um valor de nota próprio; ou seja, que não se assemelha necessariamente a um valor que outra avaliação atribuiu a essa mesma questão.
2. Também, é preciso cadastrar cada resposta de cada aluno para cada questão, de maneira que seja fácil o reconhecimento desse conjunto de informações tanto por aluno, quanto por prova (e possíveis outras fontes de pesquisa, como disciplina)
3. Por último, é preciso ramificar esses dados de maneira que se torne possível fazer análises numéricas mais diretas, como por exemplo, calcular a média de um aluno, média de nota da sala, análise de desempenho de aluno ao longo do tempo, e.c., além de poder fazer a apresentação gráfica dessa análise.

<h1>Modelo Conceitual Inicial</h1>

  Pelo diagrama criado...
