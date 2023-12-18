
CREATE DATABASE Movies;
USE Movies;

CREATE TABLE Filmes (
    id INTEGER PRIMARY KEY,
    homepage VARCHAR(255),
    adult BOOLEAN,
    budget INTEGER,
    original_language CHAR(2),
    original_title VARCHAR(50),
    overview VARCHAR(2000),
    id_coletanea INTEGER,
    title VARCHAR(50),
    runtime INTEGER,
    popularity FLOAT,
    revenue INTEGER,
    release_date DATE,
    status VARCHAR(20)
);

CREATE TABLE Avaliacao (
    id INTEGER PRIMARY KEY,
    rating FLOAT,
    timestamp TIMESTAMP,
    id_movie INTEGER
);

CREATE TABLE Coletanea (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(255)
);

CREATE TABLE Genero (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(30)
);

CREATE TABLE Atuacao (
    id_filme INTEGER,
    id_ator INTEGER,
    personagem VARCHAR(255),
    PRIMARY KEY (id_filme, id_ator)
);

CREATE TABLE Producao (
    id_filme INTEGER,
    id_produtor INTEGER,
    job VARCHAR(50),
    department VARCHAR(50),
    PRIMARY KEY (id_filme, id_produtor, job)
);

CREATE TABLE genero_filme (
    id_movie INTEGER,
    id_genero INTEGER,
    PRIMARY KEY (id_movie, id_genero)
);

CREATE TABLE keywords (
    keyword VARCHAR(50),
    id_movie INTEGER,
    PRIMARY KEY (keyword, id_movie)
);

CREATE TABLE Pessoa (
    id INTEGER PRIMARY KEY,
    genero INTEGER,
    nome VARCHAR(50)
);
 
ALTER TABLE Filmes ADD CONSTRAINT FK_Filmes_2
    FOREIGN KEY (id_coletanea)
    REFERENCES Coletanea (id);
 
ALTER TABLE Avaliacao ADD CONSTRAINT FK_Avaliacao_2
    FOREIGN KEY (id_movie)
    REFERENCES Filmes (id);
 
ALTER TABLE Coletanea ADD CONSTRAINT FK_Coletanea_2
    FOREIGN KEY (id)
    REFERENCES Filmes (id);
 
ALTER TABLE Atuacao ADD CONSTRAINT FK_Atuacao_2
    FOREIGN KEY (id_filme)
    REFERENCES Filmes (id);
 
ALTER TABLE Atuacao ADD CONSTRAINT FK_Atuacao_3
    FOREIGN KEY (id_ator)
    REFERENCES Pessoa (id);
 
ALTER TABLE Producao ADD CONSTRAINT FK_Producao_2
    FOREIGN KEY (id_filme)
    REFERENCES Filmes (id);
 
ALTER TABLE Producao ADD CONSTRAINT FK_Producao_3
    FOREIGN KEY (id_produtor)
    REFERENCES Pessoa (id);
 
ALTER TABLE genero_filme ADD CONSTRAINT FK_genero_filme_2
    FOREIGN KEY (id_movie)
    REFERENCES Filmes (id);
 
ALTER TABLE genero_filme ADD CONSTRAINT FK_genero_filme_3
    FOREIGN KEY (id_genero)
    REFERENCES Genero (id);
 
ALTER TABLE keywords ADD CONSTRAINT FK_keywords_2
    FOREIGN KEY (id_movie)
    REFERENCES Filmes (id);
