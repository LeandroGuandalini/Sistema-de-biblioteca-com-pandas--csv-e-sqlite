import pandas as pd
import os
import sqlite3

db_path = os.path.abspath("banco_dados/biblioteca.db")
conexao = sqlite3.connect(db_path)

# consulta 1: autores do livro "Piquenique na Estrada"
query_autores_livro = """
  SELECT a.nome AS autor, l.titulo AS livro
  FROM autor a  -- ajuste de 'autores' para 'autor'
  JOIN livros_autores la ON a.id_autor = la.id_autor
  JOIN livros l ON la.id_livro = l.id_livro
  WHERE l.titulo = 'Piquenique na Estrada'
"""
df_autores_livro = pd.read_sql_query(query_autores_livro, conexao)

# Consulta 2: Livros do autor "Philip K. Dick"
query_livros_autor = """
SELECT l.titulo AS livro, a.nome AS autor
FROM livros l
JOIN livros_autores la ON l.id_livro = la.id_livro
JOIN autor a ON la.id_autor = a.id_autor 
WHERE a.nome = 'Philip K. Dick'
"""
df_livros_autor = pd.read_sql_query(query_livros_autor, conexao)

# Consulta 3: Empréstimos atuais do usuário "Pedro Vinicius"
query_emprestimos_usuario = """
SELECT e.id_livro, e.id_usuario, e.data_emprestimo, e.data_devolucao, u.nome
FROM emprestimos e
JOIN usuarios u ON e.id_usuario = u.usuario_id
WHERE u.nome = 'Pedro' AND u.sobrenome = 'Vinicius'
  AND (e.data_devolucao IS NULL)
"""
df_emprestimos_usuario = pd.read_sql_query(query_emprestimos_usuario, conexao)

conexao.close()

print(df_autores_livro.head())
print(df_livros_autor.head())
print(df_emprestimos_usuario.head())