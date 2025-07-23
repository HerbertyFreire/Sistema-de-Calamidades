import gradio as gr
import pandas as pd
from datetime import datetime
import os
from legendas import (
    tipo_area, tipo_residencia, material_piso, material_parede,
    energia_eletrica, fonte_agua, rede_esgoto, destino_lixo,
    tipo_iluminacao, abastecimento_energia, sexo, parentesco,
    cor_raca, local_nascimento, certidao_nascimento,
    registro_civil, situacao_nis, familia_grupo_social,
    faixa_renda_familiar
)
from utils import safe_int, safe_get # Importamos de utils

def criar_formulario_calamidades():
    """Cria e retorna todos os componentes de calamidades"""
    with gr.Column(visible=False) as container:
        with gr.Row():
            tipo = gr.Dropdown(
                label="Tipo da Calamidade",
                choices=["Enchente", "Terremoto", "Inundação", "Seca", "Outros"],
                interactive=True
            )
        with gr.Row():
            situacao = gr.Radio(
                label="Situação",
                choices=["Afetado", "Desalojado", "Desabrigado"],
                interactive=True
            )
        with gr.Row():
            data = gr.Textbox(label="Data da Ocorrência (DD/MM/AAAA)")
        with gr.Row():
            descricao = gr.Textbox(label="Descrição Adicional", lines=3)
        with gr.Row():
            btn_salvar = gr.Button("Salvar Calamidade", elem_id="salvar-calamidade-btn")

    return {
        "container": container,
        "tipo": tipo,
        "situacao": situacao,
        "data": data,
        "descricao": descricao,
        "btn_salvar": btn_salvar
    }


def mostrar_formulario():
    """Função para mostrar o formulário de calamidades"""
    return gr.update(visible=True)


def salvar_calamidade(tipo, situacao, data, descricao, dados_pessoa):
    """Função para salvar os dados da calamidade em um arquivo CSV com legendas"""
    try:
        def get_legenda_from_data(dicionario, db_key, default_value=''):
            # Usa safe_get para obter o valor da base de dados
            valor = safe_get(dados_pessoa, db_key, '')
            if str(valor).strip() in ('', 'nan', 'None'):
                return default_value
            # Usa safe_int para garantir que a chave para o dicionário é um inteiro
            return dicionario.get(safe_int(valor), str(valor))

        # Definir a ordem das colunas explicitamente
        ordem_colunas = [
            "data_registro", "cpf", "nome", "nis",
            "tipo_calamidade", "situacao", "data_ocorrencia", "descricao",
            "sexo", "parentesco", "cor_raca", "local_nascimento", "certidao_nascimento",
            "localidade", "logradouro", "numero", "cep",
            "localizacao_domicilio", "tipo_domicilio", "material_piso", "material_parede",
            "abastecimento_agua", "esgotamento_sanitario", "destino_lixo",
            "renda_total", "faixa_renda", "bolsa_familia"
        ]

        # Criar registro mantendo a ordem das colunas
        registro = {col: "" for col in ordem_colunas}  # Inicializa todas as colunas

        # Preencher os valores
        registro.update({
            # Dados básicos
            "data_registro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cpf": safe_get(dados_pessoa, "p_num_cpf_pessoa", ""),
            "nome": safe_get(dados_pessoa, "p_nom_pessoa", ""),
            "nis": safe_get(dados_pessoa, "p_num_nis_pessoa_atual", ""),

            # Dados da calamidade
            "tipo_calamidade": tipo,
            "situacao": situacao,
            "data_ocorrencia": data,
            "descricao": descricao,

            # Informações pessoais
            "sexo": get_legenda_from_data(sexo, "p_cod_sexo_pessoa"),
            "parentesco": get_legenda_from_data(parentesco, "p_cod_parentesco_rf_pessoa"),
            "cor_raca": get_legenda_from_data(cor_raca, "p_cod_raca_cor_pessoa"),
            "local_nascimento": get_legenda_from_data(local_nascimento, "p_cod_local_nascimento_pessoa"),
            "certidao_nascimento": get_legenda_from_data(certidao_nascimento, "p_cod_certidao_nascimento_pessoa"),

            # Informações do domicílio
            "localidade": safe_get(dados_pessoa, "d_nom_localidade_fam", ""),
            "logradouro": safe_get(dados_pessoa, "d_nom_logradouro_fam", ""),
            "numero": safe_get(dados_pessoa, "d_num_logradouro_fam", ""),
            "cep": safe_get(dados_pessoa, "d_num_cep_logradouro_fam", ""),
            "localizacao_domicilio": get_legenda_from_data(tipo_area, "d_cod_local_domic_fam"),
            "tipo_domicilio": get_legenda_from_data(tipo_residencia, "d_cod_especie_domic_fam"),
            "material_piso": get_legenda_from_data(material_piso, "d_cod_material_piso_fam"),
            "material_parede": get_legenda_from_data(material_parede, "d_cod_material_domic_fam"),
            "abastecimento_agua": get_legenda_from_data(fonte_agua, "d_cod_abaste_agua_domic_fam"),
            "esgotamento_sanitario": get_legenda_from_data(rede_esgoto, "d_cod_escoa_sanitario_domic_fam"),
            "destino_lixo": get_legenda_from_data(destino_lixo, "d_cod_destino_lixo_domic_fam"),

            # Informações econômicas
            "renda_total": safe_get(dados_pessoa, "d_vlr_renda_total_fam", ""),
            "faixa_renda": get_legenda_from_data(faixa_renda_familiar, "d_fx_rfpc"),
            "bolsa_familia": "Sim" if safe_get(dados_pessoa, "d_marc_pbf", "") == "1" else "Não"
        })

        # Criar DataFrame garantindo a ordem das colunas
        df = pd.DataFrame([registro])[ordem_colunas]

        # Definir locais para salvar
        locais_tentativa = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.dirname(__file__),
            os.path.join(os.path.expanduser("~"), "Documents")
        ]

        for local in locais_tentativa:
            try:
                arquivo_saida = os.path.join(local, "registros_calamidades.csv")

                # Verificar se o arquivo já existe
                if os.path.exists(arquivo_saida):
                    # Ler o arquivo existente garantindo a mesma ordem de colunas
                    df_existente = pd.read_csv(arquivo_saida)

                    # Garantir que as colunas existentes estejam na mesma ordem
                    colunas_existentes = [col for col in ordem_colunas if col in df_existente.columns]
                    df_existente = df_existente[colunas_existentes]

                    # Adicionar novas colunas que possam estar faltando
                    for col in ordem_colunas:
                        if col not in df_existente.columns:
                            df_existente[col] = ""

                    df_existente = df_existente[ordem_colunas]
                    df_final = pd.concat([df_existente, df], ignore_index=True)
                else:
                    df_final = df

                # Salvar mantendo a ordem das colunas
                df_final[ordem_colunas].to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
                return f"<div class='success'>Registro salvo com sucesso em: {arquivo_saida}</div>"

            except Exception as e:
                continue

        return "<div class='error'>Não foi possível salvar em nenhum local disponível</div>"

    except Exception as e:
        return f"<div class='error'>Erro ao processar: {str(e)}</div>"