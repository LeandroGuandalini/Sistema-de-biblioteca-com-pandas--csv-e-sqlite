import sqlite3

conexao = sqlite3.connect('banco_dados/biblioteca.db')

cursor = conexao.cursor()

cursor.execute("""
  CREATE TABLE IF NOT EXISTS livros (
    id_livro INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    ISBN TEXT NOT NULL,
    genero TEXT NOT NULL,
    data_publicacao TEXT NOT NULL,
    qtd_paginas INTEGER NOT NULL,
    disponibilidade INTEGER NOT NULL CHECK (disponibilidade IN (0, 1))
  );
""")

cursor.execute("""
  CREATE TABLE IF NOT EXISTS autores (
    id_autor INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    pais_origem TEXT NOT NULL
  );
""")

# faz com que a combinação dos dois campos juntos seja única (PRIMARY KEY no final)
cursor.execute("""
  CREATE TABLE IF NOT EXISTS livros_autores (
    id_livro INTEGER NOT NULL,
    id_autor INTEGER NOT NULL,
    FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
    FOREIGN KEY (id_autor) REFERENCES livros(id_autor),
    PRIMARY KEY (id_livro, id_autor)
  );
""")

cursor.execute("""
  CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    data_nascimento TEXT NOT NULL
  );
""")

cursor.execute("""
  CREATE TABLE IF NOT EXISTS emprestimos (
    id_livro INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_devolucao TEXT,
    FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(usuario_id)
  );
""")

conexao.commit()
conexao.close()

print(f"banco de dados criado com sucesso")