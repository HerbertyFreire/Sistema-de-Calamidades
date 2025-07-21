# main.py

import gradio as gr
import os
import pandas as pd # Ainda útil para pd.notna
from datetime import datetime

# Importações dos novos módulos
from config import ARQUIVO_DB, TABELA_PRINCIPAL, ARQUIVO_CSV_ORIGINAL
from auth import verificar_login, criar_arquivo_usuarios
from database import criar_tabela_e_importar_dados, obter_municipios, buscar_por_cpf_no_db
from utils import montar_tabela, safe_get, safe_int
from calamidades import criar_formulario_calamidades, mostrar_formulario, salvar_calamidade
from grupo_familiar import mostrar_grupo_familiar
from legendas import (
    tipo_area, tipo_residencia, material_piso, material_parede,
    energia_eletrica, fonte_agua, rede_esgoto, destino_lixo,
    tipo_iluminacao, abastecimento_energia, sexo, parentesco,
    cor_raca, local_nascimento, certidao_nascimento,
    faixa_renda_familiar
)
from legendas_municipios import municipios_alagoas


# Variável global para armazenar os dados da pessoa atualmente pesquisada
dados_pessoa_global = {}

# Certifique-se de que o banco de dados está criado e populado ao iniciar a aplicação
# Você pode chamar isso aqui ou ter um script separado para isso.
# Para este exemplo, vamos chamar aqui, mas apenas se o DB não existir.
if not os.path.exists(ARQUIVO_DB):
    print("Banco de dados não encontrado. Iniciando criação e importação...")
    criar_tabela_e_importar_dados(ARQUIVO_CSV_ORIGINAL)
else:
    print("Banco de dados já existe. Pulando a criação e importação.")


# Obtém a lista de municípios uma vez no início da aplicação
lista_municipios = obter_municipios()


# Funções de controle de UI e dados
def handle_buscar_cpf(cpf, municipio_selecionado_valor, estado):
    """
    Função principal de busca por CPF, agora mais enxuta e chamando database.py.
    """
    if not estado["autenticado"]:
        return "<div class='error'>Acesso não autorizado. Faça login primeiro.</div>", \
               gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    global dados_pessoa_global # Acessa a variável global

    cpf = ''.join(filter(str.isdigit, cpf))
    if not cpf:
        return "<div class='error'>Por favor, informe um CPF válido.</div>", \
               gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    try:
        resultado_db_dict, colunas_db = buscar_por_cpf_no_db(cpf, municipio_selecionado_valor)

        if not resultado_db_dict:
            msg = "<div class='error'>CPF não encontrado"
            if municipio_selecionado_valor and municipio_selecionado_valor != '':
                nome_municipio = municipios_alagoas.get(municipio_selecionado_valor, "desconhecido")
                msg += f" no município de {nome_municipio} (IBGE: {municipio_selecionado_valor})"
            msg += ".</div>"
            return msg, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

        # Armazena os dados completos da pessoa no dicionário global
        dados_pessoa_global = resultado_db_dict.copy()

        # Organiza os dados em categorias usando safe_get e safe_int de utils
        pessoais = {
            'Nome': safe_get(dados_pessoa_global, 'p_nom_pessoa'),
            'NIS': safe_get(dados_pessoa_global, 'p_num_nis_pessoa_atual'),
            'Sexo': sexo.get(safe_int(safe_get(dados_pessoa_global, 'p_cod_sexo_pessoa')), ''),
            'Parentesco': parentesco.get(safe_int(safe_get(dados_pessoa_global, 'p_cod_parentesco_rf_pessoa')), ''),
            'Nome da Mãe': safe_get(dados_pessoa_global, 'p_nom_completo_mae_pessoa'),
            'Nome do Pai': safe_get(dados_pessoa_global, 'p_nom_completo_pai_pessoa'),
            'Local de Nascimento': local_nascimento.get(safe_int(safe_get(dados_pessoa_global, 'p_cod_local_nascimento_pessoa')), ''),
            'Data da Entrevista': safe_get(dados_pessoa_global, 'd_dta_entrevista_fam'),
            'Código Familiar': safe_get(dados_pessoa_global, 'd_cod_familiar_fam'),
            'Logradouro': safe_get(dados_pessoa_global, 'd_nom_logradouro_fam')
        }

        renda = {
            'Renda Média Familiar': safe_get(dados_pessoa_global, 'd_vlr_renda_media_fam'),
            'Faixa de Renda (RFPC)': faixa_renda_familiar.get(safe_int(safe_get(dados_pessoa_global, 'd_fx_rfpc')), ''),
            'Renda Total Familiar': safe_get(dados_pessoa_global, 'd_vlr_renda_total_fam'),
            'Bolsa Família': 'Sim' if safe_get(dados_pessoa_global, 'd_marc_pbf') == '1' else 'Não'
        }

        domicilio = {
            'Localidade': safe_get(dados_pessoa_global, 'd_nom_localidade_fam'),
            'Tipo de Logradouro': safe_get(dados_pessoa_global, 'd_nom_tip_logradouro_fam'),
            'Título do Logradouro': safe_get(dados_pessoa_global, 'd_nom_titulo_logradouro_fam'),
            'Nome do Logradouro': safe_get(dados_pessoa_global, 'd_nom_logradouro_fam'),
            'Número do Logradouro': safe_get(dados_pessoa_global, 'd_num_logradouro_fam'),
            'Complemento': safe_get(dados_pessoa_global, 'd_des_complemento_fam'),
            'Complemento Adicional': safe_get(dados_pessoa_global, 'd_des_complemento_adic_fam'),
            'CEP': safe_get(dados_pessoa_global, 'd_num_cep_logradouro_fam'),
            'Localização do Domicílio': tipo_area.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_local_domic_fam')), ''),
            'Tipo de Domicílio': tipo_residencia.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_especie_domic_fam')), ''),
            'Quantidade de Cômodos': safe_get(dados_pessoa_global, 'd_qtd_comodos_domic_fam'),
            'Quantidade de Dormitórios': safe_get(dados_pessoa_global, 'd_qtd_comodos_dormitorio_fam'),
            'Material do Piso': material_piso.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_material_piso_fam')), ''),
            'Material do Domicílio': material_parede.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_material_domic_fam')), ''),
            'Água Canalizada': energia_eletrica.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_agua_canalizada_fam')), ''),
            'Abastecimento de Água': fonte_agua.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_abaste_agua_domic_fam')), ''),
            'Banheiro': energia_eletrica.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_banheiro_domic_fam')), ''),
            'Esgotamento Sanitário': rede_esgoto.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_escoa_sanitario_domic_fam')), ''),
            'Destino do Lixo': destino_lixo.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_destino_lixo_domic_fam')), ''),
            'Iluminação': tipo_iluminacao.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_iluminacao_domic_fam')), ''),
            'Tipo de Calçamento': abastecimento_energia.get(safe_int(safe_get(dados_pessoa_global, 'd_cod_calcamento_domic_fam')), '')
        }

        html_result = f"""
        <div class='grid'>
            {montar_tabela("Informações Pessoais", pessoais)}
            {montar_tabela("Informações de Renda", renda)}
            {montar_tabela("Informações do Domicílio", domicilio)}
        </div>
        """

        return html_result, gr.update(visible=True), gr.update(visible=False), gr.update(visible=True)

    except Exception as e:
        return f"<div class='error'>Ocorreu um erro ao buscar o CPF: {str(e)}</div>", \
               gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)


# Interface principal Gradio
with gr.Blocks(title="Sistema de Consulta Cadastral", css="""
    /* Estilos do login */
    #login-container {
        max-width: 500px;
        margin: 40px auto;
        padding: 30px;
        background-color: #2e2e35;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }

    #login-btn {
        background-color: #ff5a1f;
        color: white;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        margin-top: 20px;
        width: 100%;
    }

    #login-btn:hover {
        background-color: #e14c12;
    }

    #logout-btn {
        background-color: #dc3545;
        color: white;
        font-weight: bold;
        padding: 8px 16px;
        border-radius: 8px;
        border: none;
    }

    .user-info {
        background-color: #2e2e35;
        padding: 10px 15px;
        border-radius: 8px;
        color: white;
        margin-right: 10px;
    }

    /* Estilos existentes do sistema */
    #submit-btn {
        background-color: #ff5a1f;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    #submit-btn:hover {
        background-color: #e14c12;
    }
    #calamidades-btn {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        padding: 8px 16px;
        border-radius: 8px;
        border: none;
        font-size: 14px;
        width: auto;
    }
    #calamidades-btn:hover {
        background-color: #218838;
    }
    #grupo-familiar-btn {
        background-color: #17a2b8;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    #grupo-familiar-btn:hover {
        background-color: #138496;
    }
    #salvar-calamidade-btn {
        background-color: #17a2b8;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    #salvar-calamidade-btn:hover {
        background-color: #138496;
    }
    .grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 20px;
    }
    .card {
        background-color: #2e2e35;
        color: white;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        flex: 1;
        min-width: 280px;
    }
    .card h4 {
        margin-top: 0;
        border-bottom: 1px solid #555;
        padding-bottom: 6px;
    }
    .card table {
        width: 100%;
        border-collapse: collapse;
    }
    .card table th,
    .card table td {
        padding: 8px;
        border-bottom: 1px solid #444;
    }
    .card table th {
        text-align: left;
        font-weight: bold;
        color: #ffb87a;
    }
    .error {
        color: #ff4444;
        font-weight: bold;
        padding: 10px;
        background-color: #ffeeee;
        border-radius: 5px;
        border: 1px solid #ffcccc;
    }
    .success {
        color: #00aa00;
        font-weight: bold;
        padding: 10px;
        background-color: #eeffee;
        border-radius: 5px;
        border: 1px solid #ccffcc;
    }
    .gr-row {
        align-items: center;
        gap: 10px;
    }
    .filter-row {
        background-color: #3a3a42;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
""") as app:
    # Estado da aplicação
    estado = gr.State({"autenticado": False, "usuario": "", "nivel_acesso": 0})

    # Tela de login
    with gr.Column(visible=True) as login_col:
        with gr.Column(elem_id="login-container"):
            gr.Markdown("## 🔒 Acesso ao Sistema de Consulta Cadastral")
            usuario_input = gr.Textbox(label="Usuário", placeholder="Digite seu nome de usuário")
            senha_input = gr.Textbox(label="Senha", type="password", placeholder="Digite sua senha")
            login_btn = gr.Button("Entrar", elem_id="login-btn")
            login_status = gr.HTML()

    # Tela principal (oculta inicialmente)
    with gr.Column(visible=False) as main_col:
        # Barra superior
        with gr.Row():
            user_info = gr.Markdown("", elem_classes="user-info")
            logout_btn = gr.Button("Sair", elem_id="logout-btn")

        # Interface original do sistema
        with gr.Blocks() as sistema:
            gr.Markdown("## 🔍 Consulta de CPF em Base de Dados")
            gr.Markdown("Digite o CPF para consultar os dados cadastrais:")

            # Filtro de município por código IBGE
            with gr.Row(elem_classes="filter-row"):
                municipio_dropdown = gr.Dropdown(
                    label="Filtrar por Município",
                    choices=lista_municipios,
                    value='',
                    interactive=True
                )

            with gr.Row():
                cpf_input = gr.Textbox(label="Digite o CPF (somente números)", lines=1)
                clear_btn = gr.Button("Limpar")
                submit_btn = gr.Button("Buscar", elem_id="submit-btn")

            with gr.Row():
                grupo_familiar_btn = gr.Button("Grupo Familiar",
                                               elem_id="grupo-familiar-btn",
                                               visible=False)
                calamidades_btn = gr.Button("Adicionar Calamidades",
                                            elem_id="calamidades-btn",
                                            visible=False)

            resultado_html = gr.HTML()
            grupo_familiar_html = gr.HTML()

            componentes_calamidades = criar_formulario_calamidades()
            calamidades_form = componentes_calamidades["container"]


    # Funções de controle de login/logout (passam o estado)
    def realizar_login(username, password, estado):
        valido, nome, nivel = verificar_login(username, password)
        if valido:
            estado.update({"autenticado": True, "usuario": nome, "nivel_acesso": nivel})
            return (
                gr.update(visible=False), # login_col
                gr.update(visible=True),  # main_col
                f"<div class='success'>Bem-vindo, {nome}!</div>", # login_status
                f"Usuário: {nome} | Nível: {'Admin' if nivel == 2 else 'Padrão'}" # user_info
            )
        else:
            estado.update({"autenticado": False, "usuario": "", "nivel_acesso": 0})
            return (
                gr.update(visible=True),  # login_col
                gr.update(visible=False), # main_col
                "<div class='error'>Usuário ou senha incorretos</div>", # login_status
                "" # user_info
            )


    def fazer_logout(estado):
        estado.update({"autenticado": False, "usuario": "", "nivel_acesso": 0})
        return (
            gr.update(visible=True),  # login_col
            gr.update(visible=False), # main_col
            "", # login_status
            "" # user_info
        )


    # Eventos da UI
    login_btn.click(
        fn=realizar_login,
        inputs=[usuario_input, senha_input, estado],
        outputs=[login_col, main_col, login_status, user_info]
    )

    logout_btn.click(
        fn=fazer_logout,
        inputs=[estado],
        outputs=[login_col, main_col, login_status, user_info]
    )

    submit_btn.click(
        fn=handle_buscar_cpf, # Agora chama a função mais limpa
        inputs=[cpf_input, municipio_dropdown, estado],
        outputs=[resultado_html, calamidades_btn, calamidades_form, grupo_familiar_btn]
    )

    calamidades_btn.click(
        fn=mostrar_formulario,
        outputs=calamidades_form
    )

    grupo_familiar_btn.click(
        fn=lambda: mostrar_grupo_familiar(dados_pessoa_global), # dados_pessoa_global já contém os dados
        outputs=grupo_familiar_html
    )

    componentes_calamidades["btn_salvar"].click(
        fn=lambda t, s, d, desc: salvar_calamidade(t, s, d, desc, dados_pessoa_global),
        inputs=[
            componentes_calamidades["tipo"],
            componentes_calamidades["situacao"],
            componentes_calamidades["data"],
            componentes_calamidades["descricao"]
        ],
        outputs=resultado_html
    )

    # Limpar campos e esconder elementos
    clear_btn.click(fn=lambda: "", outputs=cpf_input)
    clear_btn.click(fn=lambda: "", outputs=resultado_html)
    clear_btn.click(fn=lambda: gr.update(visible=False), outputs=calamidades_btn)
    clear_btn.click(fn=lambda: gr.update(visible=False), outputs=calamidades_form)
    clear_btn.click(fn=lambda: gr.update(visible=False), outputs=grupo_familiar_btn)
    clear_btn.click(fn=lambda: "", outputs=grupo_familiar_html)

# Bloco principal para iniciar a aplicação Gradio
if __name__ == "__main__":
    app.launch(share=False)