# Sistema de Consulta Cadastral (CadÚnico Simplificado)

Este projeto é um sistema de consulta cadastral que usa uma base CSV importada para SQLite e exibe os resultados por meio de uma interface web Gradio.

Ele foi organizado para ser flexível: qualquer arquivo de base no formato `tab_cad_*.csv` colocado na pasta `dados/` será detectado automaticamente e carregado em chunks.

## 📁 Estrutura do Projeto

* **`main.py`**: arquivo principal do aplicativo que abre a interface Gradio.
* **`config.py`**: configura os caminhos para a base CSV em `dados/`, o arquivo SQLite e o arquivo de usuários.
* **`database.py`**: importa o CSV para SQLite em chunks e executa as buscas.
* **`auth.py`**: cria e valida credenciais de login.
* **`calamidades.py`**: controla o registro de calamidades no sistema.
* **`grupo_familiar.py`**: busca e monta a tabela de grupo familiar.
* **`utils.py`**: funções utilitárias de formato e tratamento de dados.
* **`legendas.py`**: legendas para códigos de dados.
* **`legendas_municipios.py`**: mapeamento dos códigos IBGE para nomes de municípios.
* **`dados/`**: pasta onde a base CSV e o banco SQLite são mantidos.
* **`usuarios.txt`**: arquivo de credenciais criado automaticamente na primeira execução.

## 🚨 Importante: não subir a base para o Git

O diretório `dados/` deve ser usado apenas localmente. Não envie arquivos de base CSV ou o banco SQLite para o repositório.

Este projeto inclui um `.gitignore` que já protege os seguintes arquivos:

* `dados/*.csv`
* `dados/cadunico.db`
* `usuarios.txt`
* `__pycache__/`
* `*.pyc`

> Se você estiver usando outro repositório Git, confirme que estes caminhos também estão ignorados.

## ✅ O que precisa ser baixado / instalado

1. Python 3.8+ (recomendado Python 3.14)
2. `pandas`
3. `gradio`

Em um ambiente virtual, execute:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas gradio
```

## 📦 Como preparar a base de dados

1. Coloque seu arquivo CSV em `dados/`.
2. O nome deve seguir o padrão: `tab_cad_*.csv` (por exemplo `tab_cad_13022026_27_20260317.csv`).
3. O arquivo deve ser:
   * separado por ponto e vírgula (`;`)
   * codificado em `latin1`
   * conter as colunas usadas pelo sistema, especialmente:
     * `p_num_cpf_pessoa`
     * `d_cd_ibge`
     * `p_nom_pessoa`
     * `p_num_nis_pessoa_atual`
     * `p_cod_sexo_pessoa`
     * `p_cod_parentesco_rf_pessoa`
     * `d_cod_familiar_fam`
     * outros campos do CadÚnico usados nas buscas e exibições

## 💾 Como o carregamento funciona

O sistema carrega a base em chunks para não sobrecarregar a memória:

* `config.py` localiza automaticamente o arquivo `tab_cad_*.csv` mais recente dentro de `dados/`.
* `database.py` usa `pd.read_csv(..., chunksize=50000, on_bad_lines='skip')`.
* Cada chunk é gravado no banco SQLite `dados/cadunico.db`.
* As consultas depois são feitas diretamente no SQLite.

Se quiser forçar a recarga da base, exclua manualmente `dados/cadunico.db` e reinicie o app.

## ▶️ Como rodar o sistema

### Opção recomendada (a partir do diretório do workspace)

No PowerShell:

```powershell
cd "C:\Users\ResTIC16\OneDrive\Área de Trabalho\agora vai"
.\.venv\Scripts\Activate.ps1
python .\main.py
```

### Alternativa direta na pasta do app

```powershell
cd "C:\Users\ResTIC16\OneDrive\Área de Trabalho\agora vai\Sistema-de-Calamidades"
python main.py
```

## 🔧 Observações finais

* O arquivo `usuarios.txt` é gerado automaticamente com contas padrão:
  * `admin` / `admin123`
  * `user` / `user123`
* Se a execução encontrar o banco SQLite existente, ele não reimporta a base automaticamente.
* Converse com o código se precisar adaptar colunas diferentes: `config.py` e `database.py` são os pontos principais.

## 📌 Resumo rápido

1. Garanta o Python instalado.
2. Ative o `.venv`.
3. Instale `pandas` e `gradio`.
4. Coloque `tab_cad_*.csv` em `dados/`.
5. Execute `python .\main.py`.
6. Não suba `dados/*.csv` nem `dados/cadunico.db` para o Git.
