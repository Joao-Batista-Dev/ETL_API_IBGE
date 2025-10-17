import streamlit as st
import pandas as pd
import psycopg2
import time
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


# configuração database
POSTGRES_DBNAME=os.environ.get('POSTGRES_DBNAME')
POSTGRES_USER=os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST=os.environ.get('POSTGRES_HOST')
POSTGRES_PORT=os.environ.get('POSTGRES_PORT')


def read_database():
    try:
        conn = psycopg2.connect(
            database=POSTGRES_DBNAME,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
        query = "SELECT * FROM ibge_dados ORDER BY year DESC;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f'Error ao conectar com Banco de dados POstgreSQL: {e}')
        return pd.DataFrame()


def main():
    st.title("📊 Dashboard Populacional do Brasil - IBGE")

    df = read_database()

    if df.empty:
        st.warning("Nenhum dado encontrado no banco de dados.")
        return

    # Mostra tabela
    st.subheader("📋 Dados da População")
    st.dataframe(df)

    # Estatísticas básicas
    st.subheader("📈 Estatísticas gerais")
    st.write(df.describe())

    # Gráfico de linha
    st.subheader("📉 Crescimento populacional")
    st.line_chart(df.set_index("year")["population"])

    # Filtro de intervalo de anos
    st.subheader("🔍 Filtro de Anos")
    ano_min, ano_max = int(df["year"].min()), int(df["year"].max())
    anos = st.slider("Selecione o intervalo", ano_min, ano_max, (ano_min, ano_max))
    df_filtrado = df[(df["year"] >= anos[0]) & (df["year"] <= anos[1])]

    st.line_chart(df_filtrado.set_index("year")["population"])

    # Exibe último registro
    st.subheader("🕓 Último registro")
    st.write(df.sort_values(by="timestamp", ascending=False).head(1))


if __name__ == "__main__":
    st.set_page_config(page_title="Dashboard IBGE", layout="wide")
    main()