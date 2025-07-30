# 📊 Dashboard RH com Streamlit + PostgreSQL
Este é um pequeno sistema de visualização de dados de RH utilizando:

- PostgreSQL como banco de dados

- Python + Streamlit para interface web

- Plotly Express para gráficos interativos

## Funcionalidades:
Tabela com média salarial por departamento

Gráfico de barras com os salários acima da média

Hierarquia de cargos em gráfico de barra

## Como rodar localmente:
Clone o repositório:

bash
Copiar
Editar
git clone https://github.com/seu-usuario/nome-do-repo.git
cd nome-do-repo
##Instale as dependências:

bash
Copiar
Editar
pip install streamlit psycopg2-binary pandas plotly
Configure seu banco PostgreSQL (nome: sistema_rh) com as tabelas de funcionarios, departamentos, salarios e cargos.

## Rode o app:

bash
Copiar
Editar
streamlit run app.py
