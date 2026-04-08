# database.py
import sqlite3
import pandas as pd
import os
from config import ARQUIVO_DB, TABELA_PRINCIPAL
from legendas_municipios import municipios_alagoas
from utils import safe_int

def criar_tabela_e_importar_dados(arquivo_csv_original):
    conn = None
    try:
        # Garante que a pasta 'dados' existe antes de criar o banco
        os.makedirs(os.path.dirname(ARQUIVO_DB), exist_ok=True)
        
        conn = sqlite3.connect(ARQUIVO_DB)
        cursor = conn.cursor()

        if not os.path.exists(arquivo_csv_original):
            print(f"Erro: Arquivo CSV não encontrado em: {arquivo_csv_original}")
            return

        print("Lendo cabeçalhos e criando tabela...")
        df_temp = pd.read_csv(arquivo_csv_original, sep=';', encoding='latin1', nrows=5, dtype=str, on_bad_lines='skip')
        df_temp.columns = df_temp.columns.str.strip()
        colunas = [col.replace(".", "_") for col in df_temp.columns]

        colunas_sql = ', '.join([f'"{col}" TEXT' for col in colunas])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABELA_PRINCIPAL} ({colunas_sql})")
        conn.commit()

        print("Importando dados por partes (chunks)...")
        chunks = pd.read_csv(arquivo_csv_original, dtype=str, encoding='latin1', sep=';', chunksize=50000, on_bad_lines='skip')

        for i, chunk in enumerate(chunks):
            chunk.columns = chunk.columns.str.strip().str.replace(".", "_")
            chunk.to_sql(TABELA_PRINCIPAL, conn, if_exists='append', index=False)
            print(f"Lote {i+1} importado...")

        print("Sucesso: Banco de dados pronto!")

    except Exception as e:
        print(f"Erro na importação: {e}")
    finally:
        if conn: conn.close()

def obter_municipios():
    if not os.path.exists(ARQUIVO_DB):
        return [('Todos os municípios', '')]
    try:
        with sqlite3.connect(ARQUIVO_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT DISTINCT d_cd_ibge FROM {TABELA_PRINCIPAL} WHERE d_cd_ibge IS NOT NULL AND d_cd_ibge != ''")
            municipios_db = [str(row[0]).strip() for row in cursor.fetchall()]
        
        formatados = [('Todos os municípios', '')]
        for cod in sorted(list(set(municipios_db))):
            nome = municipios_alagoas.get(cod, "Desconhecido")
            formatados.append((f"{nome} ({cod})", cod))
        return formatados
    except:
        return [('Todos os municípios', '')]

def buscar_por_cpf_no_db(cpf, municipio_val):
    with sqlite3.connect(ARQUIVO_DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = f"SELECT * FROM {TABELA_PRINCIPAL} WHERE p_num_cpf_pessoa = ?"
        params = [cpf]
        if municipio_val:
            query += " AND d_cd_ibge = ?"
            params.append(municipio_val)
        cursor.execute(query, params)
        row = cursor.fetchone()
        return (dict(row), list(row.keys())) if row else (None, [])
