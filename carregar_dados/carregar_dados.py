import pandas as pd
import sqlite3
import os
from funcoes_aux import *

db_path = os.path.abspath("banco_dados/biblioteca.db")

conexao = sqlite3.connect(db_path)

df_livros = carregar_csv("livros.csv")
df_autores = carregar_csv("autores.csv")
df_livros_autores = carregar_csv("livros_autores.csv")
df_usuarios = carregar_csv("usuarios.csv")
df_emprestimos = carregar_csv("emprestimos.csv")

df_livros = validar_livros(df_livros)
df_autores = validar_autores(df_autores)
df_usuarios = validar_usuarios(df_usuarios)

livros_ids = df_livros['id_livro'].unique()
autores_ids = df_autores['id_autor'].unique()
usuarios_ids = df_usuarios['usuario_id'].unique()

df_livros_autores = validar_livros_autores(df_livros_autores, livros_ids, autores_ids)
df_emprestimos = validar_emprestimos(df_emprestimos, livros_ids, usuarios_ids)


df_livros.to_sql("livros", conexao, if_exists="append", index=False)
df_autores.to_sql("autor", conexao, if_exists="append", index=False)
df_livros_autores.to_sql("livros_autores", conexao, if_exists="append", index=False)
df_usuarios.to_sql("usuarios", conexao, if_exists="append", index=False)
df_emprestimos.to_sql("emprestimos", conexao, if_exists="append", index=False)


conexao.commit()
conexao.close()

print("Dados carregados com sucesso no banco de dados.")