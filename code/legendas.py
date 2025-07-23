# legendas.py

# Registro Civil e visita domiciliar
registro_civil = {
    0: "Informação migrada como inexistente",
    1: "Sem visita domiciliar",
    2: "Com visita domiciliar",
    3: "Cadastrado",
    5: "Aguardando NIS",
    6: "Validando NIS"
}

# Faixa de renda familiar (exemplo de renda mensal domiciliar)
faixa_renda_familiar = {
    1: "Até R$89,00",
    2: "Entre R$85,01 até R$178,00",
    3: "Entre R$178,01 até 1/2 salário mínimo",
    4: "Acima de 1/2 salário mínimo"
}

# Indicadores sim/não
sim_nao = {
    0: "Não",
    1: "Sim"
}

# Tempo em meses (vários usos)
tempo_meses = {
    0: "até 12 meses",
    1: "13 a 18 meses",
    2: "19 a 24 meses",
    3: "25 a 36 meses",
    4: "37 a 48 meses",
    5: "acima de 48 meses"
}

# Tipo de área
tipo_area = {
    1: "Urbanas",
    2: "Rurais"
}

# Tipo de residência
tipo_residencia = {
    1: "Particular Permanente",
    2: "Particular improvisado",
    3: "Coletivo"
}

# Material do piso
material_piso = {
    1: "Terra",
    2: "Cimento",
    3: "Madeira aproveitada",
    4: "Madeira aparelhada",
    5: "Cerâmica, lajota ou pedra",
    6: "Carpete",
    7: "Outro Material"
}

# Material da parede
material_parede = {
    1: "Alvenaria/tijolo com revestimento",
    2: "Alvenaria/tijolo sem revestimento",
    3: "Madeira aparelhada",
    4: "Taipa revestida",
    5: "Taipa não revestida",
    6: "Madeira aproveitada",
    7: "Palha",
    8: "Outro Material"
}

# Possui energia elétrica?
energia_eletrica = {
    1: "Sim",
    2: "Não"
}

# Fonte de água
fonte_agua = {
    1: "Rede geral de distribuição",
    2: "Poço ou nascente",
    3: "Cisterna",
    4: "Outra forma"
}

# Rede coletora de esgoto
rede_esgoto = {
    1: "Rede coletora de esgoto ou pluvial",
    2: "Fossa séptica",
    3: "Fossa rudimentar",
    4: "Vala a céu aberto",
    5: "Direto para um rio, lago ou mar",
    6: "Outra forma"
}

# Destino do lixo
destino_lixo = {
    1: "É coletado diretamente",
    2: "É coletado indiretamente",
    3: "É queimado ou enterrado na propriedade",
    4: "É jogado em terreno baldio ou logradouro (rua, avenida, etc.)",
    5: "É jogado em rio ou mar",
    6: "Tem outro destino"
}

# Tipo de iluminação
tipo_iluminacao = {
    1: "Elétrica com medidor próprio",
    2: "Elétrica com medidor comunitário",
    3: "Elétrica sem medidor",
    4: "Óleo, querosene ou gás",
    5: "Vela",
    6: "Outra forma"
}

# Grau de abastecimento de energia
abastecimento_energia = {
    1: "Total",
    2: "Parcial",
    3: "Não existe"
}

# Tipo de telefone (telefone fixo, celular, etc)
tipo_telefone = {
    'L': "Celular",
    'C': "Trabalho",
    'R': "Residencial",
    'O': "Recado",
    'N': "Não tem",
    'D': "Não declarado",
    'S': "Sem coleta de dados"
}

# Família por grupo social
familia_grupo_social = {
    0: "Nenhuma",
    101: "Família Cigana",
    201: "Família Extrativista",
    202: "Família de Pescadores Artesanais",
    203: "Família Pertencente a Comunidade de Terreiro",
    204: "Família Ribeirinha",
    205: "Família Agricultores Familiares",
    301: "Família Assentada da Reforma Agrária",
    302: "Família Beneficiária do Programa Nacional do Crédito Fundiário",
    303: "Família Acampada",
    304: "Família Atingida por Empreendimentos de Infraestrutura",
    305: "Família de Preso do Sistema Carcerário",
    306: "Família Catadores de Material Reciclável"
}

# Situação do NIS (Número de Identificação Social)
situacao_nis = {
    2: "Sem Registro Civil",
    3: "Cadastrado",
    5: "Aguardando NIS",
    6: "Validando NIS"
}

# Sexo
sexo = {
    1: "Masculino",
    2: "Feminino"
}

# Parentesco
parentesco = {
    1: "Pessoa Responsável pela Unidade Familiar - RF",
    2: "Cônjuge ou companheiro(a)",
    3: "Filho(a)",
    4: "Enteado(a)",
    5: "Neto(a) ou bisneto(a)",
    6: "Pai ou mãe",
    7: "Sogro(a)",
    8: "Irmão ou irmã",
    9: "Genro ou nora",
    10: "Outro parente",
    11: "Não parente"
}

# Cor ou raça
cor_raca = {
    1: "Branca",
    2: "Preta",
    3: "Amarela",
    4: "Parda",
    5: "Indígena"
}

# Local de nascimento
local_nascimento = {
    1: "Neste município",
    2: "Em outro município",
    3: "Em outro país"
}

# Possui certidão de nascimento?
certidao_nascimento = {
    1: "Sim e tem Certidão de Nascimento",
    2: "Sim, mas não tem Certidão de Nascimento",
    3: "Não",
    4: "Não sabe"
}

# Faixa etária (idade)
faixa_etaria = {
    0: "Entre 0 e 4",
    1: "Entre 5 a 6",
    2: "Entre 7 a 15",
    3: "Entre 16 a 17",
    4: "Entre 18 a 24",
    5: "Entre 25 a 34",
    6: "Entre 35 a 39",
    7: "Entre 40 a 44",
    8: "Entre 45 a 49",
    9: "Entre 50 a 54",
    10: "Entre 55 a 59",
    11: "Entre 60 a 64",
    12: "Maior que 65"
}

# Evento registral
evento_registral = {
    1: "Nascimento",
    2: "Casamento",
    3: "RANI"
}

# Opções marcadas no formulário
opcao_formulario = {
    0: "Opção não marcada no formulário",
    1: "Opção marcada no formulário"
}

# Frequência de uso (exemplo: frequência de acesso ou uso)
frequencia = {
    1: "Todo dia",
    2: "Toda semana",
    3: "Todo mês",
    4: "Todo ano",
    5: "Quase nunca",
    6: "Nunca"
}

# Identidade de gênero (exemplo: pessoa trans, travesti)
identidade_genero = {
    1: "Sim, a pessoa é trans",
    2: "Sim, a pessoa é travesti",
    3: "Não"
}

# Gênero autodeclarado
genero_autodeclarado = {
    1: "Feminina",
    2: "Masculina",
    3: "Não binário/a"
}

# Tempo de moradia (em anos)
tempo_moradia_anos = {
    1: "Até seis meses",
    2: "Entre seis meses e um ano",
    3: "Entre um e dois anos",
    4: "Entre dois e cinco anos",
    5: "Entre cinco e dez anos",
    6: "Mais de dez anos"
}

# Tipo de trabalho
tipo_trabalho = {
    1: "Trabalhador por conta própria (bico, autônomo)",
    2: "Trabalhador temporário em área rural",
    3: "Empregado sem carteira de trabalho assinada",
    4: "Empregado com carteira de trabalho assinada"
}