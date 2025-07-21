# utils.py

import pandas as pd

def montar_tabela(titulo, dados):
    """
    Gera um bloco HTML para exibir dados em formato de tabela.
    Movida de 'Codigo.py'.
    """
    html = f"""
    <div class="card">
        <h4>{titulo}</h4>
        <table>
            <thead><tr><th>Campo</th><th>Valor</th></tr></thead>
            <tbody>
    """
    for chave, valor in dados.items():
        if valor is not None and str(valor).lower() != 'nan' and str(valor).strip() != '':
            html += f"<tr><td>{chave}</td><td>{valor}</td></tr>"
    html += "</tbody></table></div>"
    return html

def safe_get(data_dict, key, default=''):
    """
    Função auxiliar para obter valores com segurança de um dicionário,
    ajustando para nomes de colunas do DB e tratando NaN.
    Movida de 'Codigo.py'.
    """
    # As chaves do CSV (ex: p.nom_pessoa) viram p_nom_pessoa no DB
    db_key = key.replace('.', '_')
    value = data_dict.get(db_key, default)
    return value if pd.notna(value) else default

def safe_int(value, default=0):
    """
    Converte um valor para inteiro com tratamento de erros.
    Movida de 'Codigo.py'.
    """
    try:
        # Tenta converter para float primeiro para lidar com strings como "1.0"
        return int(float(value)) if str(value).strip() else default
    except (ValueError, TypeError):
        return default