DROP DATABASE IF EXISTS provas_avaliacao;

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

CREATE TABLE disciplinas(
	cpf VARCHAR(11) NOT NULL,
	disciplina VARCHAR(100) NOT NULL,
	CONSTRAINT "pk_disc" PRIMARY KEY (cpf,disciplina),
	CONSTRAINT "fk_disc_aluno" FOREIGN KEY(cpf)
	REFERENCES aluno(cpf)
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
	nota_final INTEGER NOT NULL CHECK (nota_final BETWEEN 0 AND 10),
	disciplina VARCHAR(100),
	p_cpf VARCHAR(11) NOT NULL,
	a_cpf VARCHAR(11) NOT NULL,
	CONSTRAINT "pk_ava" PRIMARY KEY(cod),
	CONSTRAINT "fk_ava_prof" FOREIGN KEY(p_cpf)
	REFERENCES professor(cpf),
	CONSTRAINT "fk_ava_aluno" FOREIGN KEY(a_cpf)
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




