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

A modelagem foi feita em três etapas:

<h3>Modelo Conceitual</h3>

![Modelo Conceitual](01%20-%20Diagramas/Conceito_03.jpg)

O diagrama ER ilustra as entidades principais (Professor, Aluno, Disciplina, Avaliação, Questão, Resposta Dada) e seus relacionamentos (ministra, aplica, cursa, utiliza, realiza).

<h3>Modelo Lógico</h3>

	Professor(CPF*, nome, data_nasc, salario, idade)	
	Aluno(CPF*, nome, turma, semestre)  
	Disciplina(COD*, nome, descricao, CPF_Professor**)
	Avaliacao(COD*, descricao, data, horario, valor_total, COD_Disciplina**)
	Questao(COD*, tipo, pergunta)
	Q_Objetiva(COD**, resposta_certa)
	Q_Descritiva(COD**, resposta_esperada) 
	Opcao(COD_Questao**, letra*, opcao_texto)
	Questao_Usada(COD_Avaliacao**, COD_Questao**, valor)
	Aluno_Cursa_Disciplina(CPF_Aluno**, COD_Disciplina**)
	Prova_Feita(CPF_Aluno**, COD_Avaliacao**, nota_final)
	Resposta_Dada(CPF_Aluno**, COD_Avaliacao**, COD_Questao**, resposta, nota_questao)
    
    * = chave primaria
    ** = chave estrangeira 




A transcrição acima (do modelo conceitual) traduzido a sua dinâmica de forma normalizada, com todas as chaves primárias e estrangeiras devidamente indicadas.

E por último, mas não menos importante,

<h3>Modelo Físico</h3>

    CREATE DATABASE provas_avaliacao;
    
    CREATE TABLE professor(
    	cpf VARCHAR(11) NOT NULL,
    	nome VARCHAR(100) NOT NULL,
    	data_nasc DATE,
    	salario NUMERIC(10, 2) NOT NULL CHECK (salario > 0),
    	idade INTEGER NOT NULL CHECK (idade BETWEEN 0 AND 100),
    	CONSTRAINT "pk_prof" PRIMARY KEY (cpf)
    );
    
    CREATE TABLE aluno(
    	cpf VARCHAR(11) NOT NULL,
    	nome VARCHAR(100) NOT NULL,
    	turma VARCHAR(100) NOT NULL,
    	semestre INTEGER NOT NULL CHECK (semestre BETWEEN 1 AND 10),
    	CONSTRAINT "pk_aluno" PRIMARY KEY (cpf)
    );
    
    CREATE TABLE disciplina(
    	cod INTEGER NOT NULL,
    	cpf VARCHAR(11) NOT NULL,
    	nome VARCHAR(100) NOT NULL,
    	descricao VARCHAR(300) NOT NULL,
    	CONSTRAINT "pk_disc" PRIMARY KEY (cod),
    	CONSTRAINT "fk_disc_aluno" FOREIGN KEY(cpf)
    	REFERENCES professor(cpf)
    );
    
    CREATE TABLE questao(
    	cod INTEGER NOT NULL,
    	tipo VARCHAR(10) NOT NULL,
    	pergunta VARCHAR(300),
    	CONSTRAINT "pk_ques" PRIMARY KEY (cod)
    );
    
    CREATE TABLE q_descritiva(
    	resposta_esperada VARCHAR(300),
    	CONSTRAINT "pk_q_descritiva" PRIMARY KEY (cod)
    ) INHERITS(questao);
    
    CREATE TABLE q_objetiva(
    	resposta_certa VARCHAR(1),
    	CONSTRAINT "pk_q_objetiva" PRIMARY KEY (cod)
    ) INHERITS(questao);
    
    CREATE TABLE opcoes(
    	cod INTEGER NOT NULL,
    	opcao VARCHAR(300) NOT NULL,
    	CONSTRAINT "pk_opcoes" PRIMARY KEY(cod, opcao),
    	CONSTRAINT "fk_opcoes_questoes" FOREIGN KEY(cod)
    	REFERENCES questoes(cod)
    );
    
    CREATE TABLE avaliacao(
    	cod INTEGER NOT NULL,
    	descricao VARCHAR(300) NOT NULL,
    	data DATE NOT NULL,
    	horario TIME NOT NULL,
    	valor INTEGER NOT NULL CHECK (valor > 0),
    	p_cpf VARCHAR(11) NOT NULL,
    	CONSTRAINT "pk_ava" PRIMARY KEY(cod),
    	CONSTRAINT "fk_ava_prof" FOREIGN KEY(p_cpf)
    	REFERENCES professor(cpf)
    );	
    
    CREATE TABLE prova_feita(
    	cod INTEGER NOT NULL,
    	cpf VARCHAR(11) NOT NULL,
    	nota_final INTEGER NOT NULL CHECK (nota_final BETWEEN 0 AND 10),
    	CONSTRAINT "pk_prova" PRIMARY KEY(cod, cpf),
    	CONSTRAINT "fk_prova_ava" FOREIGN KEY(cod)
    	REFERENCES avaliacao(cod),
    	CONSTRAINT "fk_prova_aluno" FOREIGN KEY(cpf)
    	REFERENCES aluno(cpf)
    );
    CREATE TABLE questoes_usadas(
    	a_cod INTEGER NOT NULL,
    	q_cod INTEGER NOT NULL,
    	valor INTEGER NOT NULL CHECK (valor > 0),
    	CONSTRAINT "pk_ques_usadas" PRIMARY KEY (a_cod, q_cod),
    	CONSTRAINT "fk_ques_usadas_ava" FOREIGN KEY(a_cod)
    	REFERENCES avaliacao(cod),
    	CONSTRAINT "fk_ques_usadas_ques" FOREIGN KEY(q_cod)
    	REFERENCES questao(cod)
    );
    
    CREATE TABLE aluno_cursa_disc(
    	cod INTEGER NOT NULL,
    	cpf VARCHAR(11) NOT NULL,
    	CONSTRAINT "pk_acd" FOREIGN KEY(cod, cpf),
    	CONSTRAINT "fk_acd_disc" FOREIGN KEY(cod)
    	REFERENCES disciplina(cod),
    	CONSTRAINT "fk_acd_aluno" FOREIGN KEY(cpf)
    	REFERENCES aluno(cod)
    );
    
    CREATE TABLE resposta_dada(
    	cpf VARCHAR(11) NOT NULL,
    	a_cod INTEGER NOT NULL,
    	q_cod INTEGER NOT NULL,
    	resposta VARCHAR(300) NOT NULL,
    	nota_final INTEGER NOT NULL CHECK (nota_final BETWEEN 0 AND 10),
    	CONSTRAINT "pk_res" PRIMARY KEY (cpf, a_cod, q_cod),
    	CONSTRAINT "fk_res_aluno" FOREIGN KEY(cpf)
    	REFERENCES aluno(cpf),
    	CONSTRAINT "fk_res_ava" FOREIGN KEY(a_cod)
    	REFERENCES avaliacao(cod),
    	CONSTRAINT "fk_res_ques" FOREIGN KEY(q_cod)
    	REFERENCES questao(cod)
	
Implementamos nosso banco de dados em PostgreSQL, com todas as restrições de integridade e domínio (como CHECK, NOT NULL, e FOREIGN KEY).

<h1>Resultato e Prospecção</h1>

Com a lógica que adotamos no modelo, é possível realizar consultas e operações que envolvem o cruzamento direto entre alunos, disciplinas, avaliações e questões.

A estrutura relacional foi pensada para permitir o cálculo de médias por aluno, turma ou disciplina, a análise de desempenho ao longo do tempo, e a comparação entre diferentes avaliações. Além disso, a normalização garante consistência e integridade dos dados, facilitando a implementação de relatórios e gráficos no sistema final, como evolução de notas, distribuição de acertos por questão e estatísticas gerais de aproveitamento.
