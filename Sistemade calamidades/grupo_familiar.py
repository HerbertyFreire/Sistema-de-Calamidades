import pandas as pd
import gradio as gr
import sqlite3
from legendas import parentesco
from config import ARQUIVO_DB, TABELA_PRINCIPAL # Importar do config
from utils import safe_int # Importar safe_int de utils


def buscar_grupo_familiar(cod_familiar, arquivo_db, tabela_nome):
    """
    Busca e formata as informações do grupo familiar de um código familiar.
    """
    try:
        conn = sqlite3.connect(arquivo_db)
        cursor = conn.cursor()

        coluna_cod_familiar_db = 'd_cod_familiar_fam'

        # Query para selecionar os membros do grupo familiar
        query = f"SELECT p_nom_pessoa, p_num_cpf_pessoa, p_cod_parentesco_rf_pessoa, p_dta_nasc_pessoa FROM {tabela_nome} WHERE \"{coluna_cod_familiar_db}\" = ?"
        cursor.execute(query, (cod_familiar,))
        resultados_db = cursor.fetchall()
        conn.close()

        if not resultados_db:
            return "<div class='error'>Nenhum membro familiar encontrado para este código familiar.</div>"

        membros_familia_unicos = []
        chaves_ja_adicionadas = set() # Usar um set para garantir unicidade com uma chave composta

        for membro_tuple in resultados_db:
            # Obtém os dados e garante que são strings para a chave composta
            nome_membro = str(membro_tuple[0]).strip() if membro_tuple[0] is not None else ''
            cpf_membro = str(membro_tuple[1]).strip() if membro_tuple[1] is not None else ''
            parentesco_membro_codigo = str(membro_tuple[2]).strip() if membro_tuple[2] is not None else '0' # Pega o código para a chave
            data_nascimento_membro = str(membro_tuple[3]).strip() if membro_tuple[3] is not None else ''

            # Cria uma chave composta para unicidade
            # Combinação de Nome, CPF (se existir), Parentesco (código), Data de Nascimento
            chave_composta = (nome_membro, cpf_membro, parentesco_membro_codigo, data_nascimento_membro)

            # Verifica se essa chave composta já foi adicionada
            if chave_composta in chaves_ja_adicionadas:
                continue # Pula este membro se a combinação já existe

            # Se a chave não é duplicada, adiciona o membro e sua chave
            membro = {
                'Nome': nome_membro,
                'CPF': cpf_membro,
                'Parentesco': parentesco.get(safe_int(parentesco_membro_codigo), ''), # Usa safe_int aqui
                'Data Nascimento': data_nascimento_membro
            }
            membros_familia_unicos.append(membro)
            chaves_ja_adicionadas.add(chave_composta) # Adiciona a chave composta ao set


        # Início da construção do HTML
        html = """
        <div class="card">
            <h4>Grupo Familiar</h4>
            <table>
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>CPF</th>
                        <th>Parentesco</th>
                        <th>Data Nascimento</th>
                    </tr>
                </thead>
                <tbody>
        """

        # Adiciona cada membro único à tabela HTML
        for membro in membros_familia_unicos: # Itera sobre a lista de membros únicos
            html += f"""
                <tr>
                    <td>{membro['Nome']}</td>
                    <td>{membro['CPF']}</td>
                    <td>{membro['Parentesco']}</td>
                    <td>{membro['Data Nascimento']}</td>
                </tr>
            """

        html += "</tbody></table></div>"
        return html

    except Exception as e:
        return f"<div class='error'>Erro ao buscar grupo familiar: {str(e)}</div>"


def mostrar_grupo_familiar(dados_pessoa):
    """
    Função para exibir o grupo familiar de uma pessoa.
    Agora usa as configurações globais.
    """
    if not dados_pessoa:
        return "<div class='error'>Nenhum dado de pessoa disponível.</div>"

    # A chave no dicionário dados_pessoa global será d_cod_familiar_fam (nome da coluna no DB)
    cod_familiar = dados_pessoa.get('d_cod_familiar_fam')
    if not cod_familiar:
        return "<div class='error'>Código familiar não encontrado.</div>"

    # Chama buscar_grupo_familiar usando as variáveis de configuração globais
    return buscar_grupo_familiar(cod_familiar, ARQUIVO_DB, TABELA_PRINCIPAL)