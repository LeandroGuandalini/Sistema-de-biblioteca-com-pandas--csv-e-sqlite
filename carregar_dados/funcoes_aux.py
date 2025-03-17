import pandas as pd
import sqlite3
import os

def carregar_csv(nome_arquivo):
    """
    Carrega um arquivo CSV da pasta 'dados' e retorna um DataFrame.

    Args:
        nome_arquivo (str): Nome do arquivo CSV a ser carregado.

    Returns:
        pd.DataFrame: DataFrame com os dados do arquivo CSV.
    """
    caminho = os.path.join("dados", nome_arquivo)
    return pd.read_csv(caminho)


def validar_livros(df):
    """
    Valida o DataFrame de livros, removendo duplicatas, verificando campos obrigatórios e normalizando a coluna de disponibilidade.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados da tabela livros.

    Returns:
        pd.DataFrame: DataFrame validado e tratado.

    Raises:
        ValueError: Caso existam valores nulos em campos obrigatórios.
    """
    df = df.drop_duplicates(subset=['id_livro'])
    if df[['id_livro', 'titulo', 'ISBN', 'genero', 'data_publicacao', 'qtd_paginas', 'disponibilidade']].isnull().any().any():
        raise ValueError('Livros com campos obrigatórios nulos.')
    df = df[df['disponibilidade'].isin([0, 1])]
    df['disponibilidade'] = df['disponibilidade'].astype(int)
    return df


def validar_autores(df):
    """
    Valida o DataFrame de autores, removendo duplicatas e verificando campos obrigatórios.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados da tabela autor.

    Returns:
        pd.DataFrame: DataFrame validado e tratado.

    Raises:
        ValueError: Caso existam valores nulos em campos obrigatórios.
    """
    df = df.drop_duplicates(subset=['id_autor'])
    if df[['id_autor', 'nome', 'pais_origem']].isnull().any().any():
        raise ValueError('Autores com campos obrigatórios nulos.')
    return df


def validar_livros_autores(df, livros_ids, autores_ids):
    """
    Valida o DataFrame de relacionamento livros_autores, removendo duplicatas e garantindo integridade referencial.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados da tabela livros_autores.
        livros_ids (list or pd.Series): Lista de IDs de livros válidos.
        autores_ids (list or pd.Series): Lista de IDs de autores válidos.

    Returns:
        pd.DataFrame: DataFrame validado e tratado.
    """
    df = df.drop_duplicates(subset=['id_livro', 'id_autor'])
    df = df[df['id_livro'].isin(livros_ids) & df['id_autor'].isin(autores_ids)]
    return df


def validar_usuarios(df):
    """
    Valida o DataFrame de usuários, removendo duplicatas e verificando campos obrigatórios.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados da tabela usuarios.

    Returns:
        pd.DataFrame: DataFrame validado e tratado.

    Raises:
        ValueError: Caso existam valores nulos em campos obrigatórios.
    """
    df = df.drop_duplicates(subset=['usuario_id'])
    if df[['usuario_id', 'nome', 'sobrenome', 'data_nascimento']].isnull().any().any():
        raise ValueError("Usuários com campos obrigatórios nulos.")
    return df


def validar_emprestimos(df, livros_ids, usuarios_ids):
    """
    Valida o DataFrame de empréstimos, removendo duplicatas, garantindo integridade referencial e formatando datas.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados da tabela emprestimos.
        livros_ids (list or pd.Series): Lista de IDs de livros válidos.
        usuarios_ids (list or pd.Series): Lista de IDs de usuários válidos.

    Returns:
        pd.DataFrame: DataFrame validado e tratado.

    Raises:
        ValueError: Caso existam valores nulos em campos obrigatórios ou erro no formato das datas.
    """
    df = df.drop_duplicates(subset=['id_livro', 'id_usuario'])
    df = df[df['id_livro'].isin(livros_ids) & df['id_usuario'].isin(usuarios_ids)]
    df['data_emprestimo'] = pd.to_datetime(df['data_emprestimo'], format='%Y-%m-%d', errors='raise')
    df['data_devolucao'] = pd.to_datetime(df['data_devolucao'], format='%Y-%m-%d', errors='coerce')
    if df[['id_livro', 'id_usuario', 'data_emprestimo']].isnull().any().any():
        raise ValueError("Empréstimos com campos obrigatórios nulos.")
    return df
