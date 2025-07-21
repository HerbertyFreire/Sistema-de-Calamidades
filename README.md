# Sistema de Consulta Cadastral (CadÚnico Simplificado)

Este projeto é um sistema de consulta de dados cadastrais simplificado, simulando informações do CadÚnico, com funcionalidades de busca por CPF, visualização de grupo familiar e registro de calamidades, tudo através de uma interface web interativa construída com Gradio.

O código foi reestruturado para melhorar a organização, modularidade e manutenibilidade, separando as diferentes responsabilidades em módulos Python dedicados.

## 📁 Estrutura do Projeto e Módulos

O projeto está organizado em módulos Python, cada um com uma responsabilidade específica:

* **`main.py`**: Este é o **arquivo principal** do sistema. Ele contém a interface web (Gradio), a lógica de login e logout, e orquestra as chamadas para as funções dos outros módulos. É o ponto de entrada da aplicação.
* **`config.py`**: Armazena as **configurações globais** do sistema, como caminhos de arquivos (CSV original, banco de dados SQLite, arquivo de usuários) e nomes de tabelas. Centraliza as configurações para fácil modificação.
* **`auth.py`**: Contém toda a **lógica de autenticação** de usuários. Inclui funções para criar o arquivo de usuários padrão (`usuarios.txt`) e para verificar as credenciais de login.
* **`database.py`**: Responsável por todas as **interações com o banco de dados SQLite**. Possui funções para criar a tabela, importar dados do CSV, obter a lista de municípios e realizar a busca de informações por CPF.
* **`utils.py`**: Módulo para **funções utilitárias e auxiliares** gerais que podem ser reutilizadas em diversas partes do sistema, como a formatação de tabelas HTML para exibição e funções de tratamento seguro de dados.
* **`calamidades.py`**: Contém a lógica e os componentes da interface para o **formulário de registro de calamidades**. Gerencia a criação e o salvamento desses registros em um arquivo CSV separado.
* [cite_start]**`grupo_familiar.py`**: [cite: 1] Responsável por buscar e formatar as **informações do grupo familiar** de uma pessoa. Interage com o banco de dados para recuperar os membros da família e os exibe em formato de tabela.
* **`legendas.py`**: Dicionários Python que fornecem **legendas e descrições para códigos** presentes nos dados (ex: tipo de área, sexo, parentesco). Ajuda a exibir informações de forma mais legível.
* **`legendas_municipios.py`**: Um dicionário específico que mapeia os **códigos IBGE para os nomes dos municípios** de Alagoas, utilizado para filtros e exibição de dados.
* **`dados/` (Pasta)**: Diretório destinado a armazenar os arquivos de dados. Atualmente, contém o CSV original e o banco de dados SQLite que será gerado.
* **`usuarios.txt` (Arquivo)**: Criado automaticamente na primeira vez que o sistema é executado ou uma tentativa de login é feita. Armazena as credenciais de usuário (username e senha hashed) e seus níveis de acesso.

## ✨ Funcionalidades

* **Autenticação de Usuário:** Sistema de login simples com usuários e senhas pré-definidos (admin e user).
* **Consulta por CPF:** Busca detalhada de informações de pessoas em um banco de dados **SQLite**, com filtro por município.
* [cite_start]**Visualização de Grupo Familiar:** Exibe todos os membros do grupo familiar associado ao CPF pesquisado. [cite: 1]
* **Registro de Calamidades:** Permite registrar informações sobre calamidades (enchente, seca, etc.) relacionadas a um indivíduo pesquisado, salvando os dados em um arquivo CSV.
* **Interface Web Amigável:** Utiliza a biblioteca Gradio para uma interface de usuário intuitiva e fácil de usar no navegador.

## ⚙️ Pré-requisitos

Para rodar este projeto, você precisará ter o **Python instalado** em seu sistema. Recomenda-se usar o Python 3.8 ou superior.

Além disso, as seguintes bibliotecas Python são necessárias:

* `pandas`: Para manipulação e leitura de dados.
* `gradio`: Para construir a interface web interativa.
* `hashlib`: Já é uma biblioteca padrão do Python, usada para hashing de senhas.
* `sqlite3`: Já é uma biblioteca padrão do Python, usada para interagir com o banco de dados SQLite.

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o sistema:

### 1. **Clone ou Baixe o Projeto**

Certifique-se de ter todos os arquivos Python (`.py`) e o diretório `dados/` com seu arquivo CSV no local correto, conforme a "Estrutura do Projeto e Módulos" detalhada acima.

### 2. **Instale as Dependências**

Abra seu terminal ou prompt de comando e navegue até o diretório raiz do projeto (onde está o `main.py`). Em seguida, instale as bibliotecas necessárias:

```bash
pip install pandas gradio
