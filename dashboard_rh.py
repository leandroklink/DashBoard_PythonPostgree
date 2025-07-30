import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px


# Conexão com o banco PostgreSQL
def conectar():
    conn = psycopg2.connect(
        dbname="sistema_rh",  # com aspas não precisa, mas no código pode ser assim
        user="postgres",
        password="2910",
        host="localhost",
        port="5432"
    )
    conn.set_client_encoding('UTF8')
    return conn

def tratar_df(df):
    for col in df.select_dtypes(include=["object"]):
        df[col] = df[col].apply(
            lambda x: x.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore") if isinstance(x, str) else x
        )
    return df



# Consultas SQL:
def media_salarial_por_departamento(conn):
    query = """
    SELECT d.nome AS departamento, ROUND(AVG(s.valor), 2) AS media_salario
    FROM departamentos d
    JOIN funcionarios f ON d.id = f.departamento_id
    JOIN salarios s ON f.id = s.funcionario_id
    GROUP BY d.nome
    """
    return pd.read_sql_query(query, conn)

def funcionarios_salario_acima_media(conn):
    query = """
    SELECT f.nome, s.valor
    FROM funcionarios f
    JOIN salarios s ON f.id = s.funcionario_id
    WHERE s.valor > (
    SELECT AVG(valor) FROM salarios
    );
    """
    return pd.read_sql_query(query,conn)

def Hierarquia_cargos(conn):
    query = """
    SELECT nome, nivel_hierarquia
    FROM cargos
    ORDER BY nivel_hierarquia;
    """
    return pd.read_sql_query(query,conn)


# Início do app Streamlit
st.set_page_config(page_title="Dashboard RH", layout="wide")
st.title("📊 Dashboard de RH - Média Salarial")

col1, col2 = st.columns(2)


# Conectar ao banco
try:


    conn = conectar()
    # Mostrar tabela
    st.subheader("📋 Tabela: Média Salarial por Departamento")
    st.dataframe(media_salarial_por_departamento(conn))
    df = media_salarial_por_departamento(conn)


    fig = px.bar(df, x="departamento", y="media_salario",
                 title="Média Salarial por Departamento",
                 labels={"media_salario": "Salário (R$)", "departamento": "Departamento"},
                 text_auto=True)
    col1.plotly_chart(fig, use_container_width=True)


    df_acima_media = funcionarios_salario_acima_media(conn)
    fig = px.bar(df_acima_media, 
             x="valor", 
             y="nome", 
             orientation="h",  # barra horizontal
             title="Funcionários com Salário Acima da Média",
             labels={"valor": "Salário (R$)", "nome": "Funcionário"},
             text_auto=True)
    col2.plotly_chart(fig, use_container_width=True)

    df_hierarquia = Hierarquia_cargos(conn)
    fig = px.bar(df_hierarquia, 
             x="nome", 
             y="nivel_hierarquia", 
             title="Hierarquia de Cargos",
             labels={"nome": "Cargo", "nivel_hierarquia": "Nível Hierárquico"},
             text_auto=True)
    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(fig, use_container_width=True)


except Exception as e:
    st.error(f"Erro ao conectar ao banco: {e}")

finally:
    if 'conn' in locals():
        conn.close()
