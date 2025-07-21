# database.py

import sqlite3
import pandas as pd
import os
from config import ARQUIVO_DB, TABELA_PRINCIPAL
from legendas_municipios import municipios_alagoas
from utils import safe_int # Importar safe_int de utils

def criar_tabela_e_importar_dados(arquivo_csv_original):
    """
    Cria a tabela no SQLite e importa os dados de um CSV.
    Esta função foi movida de 'criar_banco_dados.py'.
    """
    conn = None
    try:
        conn = sqlite3.connect(ARQUIVO_DB)
        cursor = conn.cursor()

        print(f"Verificando arquivo CSV em: {arquivo_csv_original}")
        if not os.path.exists(arquivo_csv_original):
            print(f"Erro: Arquivo CSV não encontrado em '{arquivo_csv_original}'. Por favor, verifique o caminho.")
            return

        print("Lendo cabeçalhos do CSV para criar a estrutura da tabela...")
        df_temp = pd.read_csv(arquivo_csv_original, sep=';', encoding='latin1', nrows=5, dtype=str, on_bad_lines='skip')
        df_temp.columns = df_temp.columns.str.strip()
        colunas = df_temp.columns.tolist()

        if not colunas:
            print("Erro: Nenhuma coluna encontrada no arquivo CSV. Verifique o separador ou o formato do arquivo.")
            return

        colunas_sql = ', '.join([f'"{col.replace(".", "_")}" TEXT' for col in colunas])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {TABELA_PRINCIPAL} ({colunas_sql})"
        print(f"Criando tabela com SQL: {create_table_sql}")
        cursor.execute(create_table_sql)
        conn.commit()
        print("Tabela criada ou já existente.")

        print("Iniciando importação de dados do CSV para o SQLite...")
        chunks = pd.read_csv(
            arquivo_csv_original,
            dtype=str,
            encoding='latin1',
            sep=';',
            engine='python',
            on_bad_lines='skip',
            chunksize=50000
        )

        total_linhas_importadas = 0
        for i, chunk in enumerate(chunks):
            chunk.columns = chunk.columns.str.strip()
            chunk.columns = [col.replace(".", "_") for col in chunk.columns]

            for col in [c.replace(".", "_") for c in colunas]:
                if col not in chunk.columns:
                    chunk[col] = None
            chunk = chunk[[c.replace(".", "_") for c in colunas]]

            chunk.to_sql(TABELA_PRINCIPAL, conn, if_exists='append', index=False)
            total_linhas_importadas += len(chunk)
            print(f"Chunk {i+1} importado. Total de linhas: {total_linhas_importadas}")

        print(f"Importação concluída. Total de {total_linhas_importadas} linhas importadas para '{ARQUIVO_DB}'.")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except pd.errors.EmptyDataError:
        print(f"Erro: O arquivo CSV '{arquivo_csv_original}' está vazio.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar/importar o DB: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

def obter_municipios():
    """
    Obtém a lista de códigos IBGE e nomes de municípios do DB.
    Movida de 'Codigo.py'.
    """
    try:
        if not os.path.exists(ARQUIVO_DB):
            print(f"Erro: Banco de dados não encontrado: {ARQUIVO_DB}")
            return [('', 'Todos os municípios')]

        conn = sqlite3.connect(ARQUIVO_DB)
        cursor = conn.cursor()

        cursor.execute(f"SELECT DISTINCT d_cd_ibge FROM {TABELA_PRINCIPAL} WHERE d_cd_ibge IS NOT NULL AND d_cd_ibge != '' ORDER BY d_cd_ibge")
        municipios_db = [str(row[0]).strip() for row in cursor.fetchall()]
        conn.close()

        municipios_formatados = []
        for cod in sorted(list(set(municipios_db))):
            nome = municipios_alagoas.get(cod, "Desconhecido")
            municipios_formatados.append((f"{nome} ({cod})", cod))

        municipios_formatados.insert(0, ('Todos os municípios', ''))

        return municipios_formatados

    except Exception as e:
        print(f"Erro ao obter municípios do DB: {str(e)}")
        return [('', 'Todos os municípios')]

def buscar_por_cpf_no_db(cpf, municipio_selecionado_valor):
    """
    Busca informações de uma pessoa no banco de dados SQLite por CPF e município.
    Movida de 'Codigo.py'.
    """
    coluna_cpf_db = 'p_num_cpf_pessoa'
    coluna_ibge_db = 'd_cd_ibge'

    try:
        if not os.path.exists(ARQUIVO_DB):
            raise FileNotFoundError(f"Banco de dados não encontrado: {ARQUIVO_DB}. Por favor, execute a criação do banco de dados primeiro.")

        conn = sqlite3.connect(ARQUIVO_DB)
        cursor = conn.cursor()

        query = f"SELECT * FROM {TABELA_PRINCIPAL} WHERE \"{coluna_cpf_db}\" = ?"
        params = [cpf]

        if municipio_selecionado_valor and municipio_selecionado_valor != '':
            query += f" AND \"{coluna_ibge_db}\" = ?"
            params.append(municipio_selecionado_valor)

        cursor.execute(query, params)
        resultado_db = cursor.fetchone()
        colunas_db = [description[0] for description in cursor.description]
        conn.close()

        if not resultado_db:
            return None, colunas_db

        return dict(zip(colunas_db, resultado_db)), colunas_db

    except Exception as e:
        raise Exception(f"Erro ao buscar CPF no banco de dados: {str(e)}")