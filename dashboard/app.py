import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Weather Insights SP",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(env_path)

@st.cache_resource(ttl=600)
def get_engine():
    try:
        user = os.getenv('DB_USER')
        password = quote_plus(os.getenv('DB_PASSWORD'))
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
        
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        return create_engine(url)
    except Exception as e:
        logger.error(f"Erro ao criar engine: {e}")
        raise e

@st.cache_data(ttl=60)
def load_data():
    try:
        engine = get_engine()
        query = "SELECT * FROM public.sp_weather ORDER BY datetime DESC"
        df = pd.read_sql(query, engine)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {str(e)}")
        raise e

st.sidebar.header("Filtros e Opções")

try:
    df_raw = load_data()
    
    cidades = df_raw["city_name"].unique()
    cidade_selecionada = st.sidebar.selectbox("Selecione a Localidade", cidades)
    
    min_date = df_raw["datetime"].min().date()
    max_date = df_raw["datetime"].max().date()
    date_range = st.sidebar.date_input(
        "Periodo de Analise",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    df = df_raw[df_raw["city_name"] == cidade_selecionada]
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)]

    st.title(f"Weather Insights: {cidade_selecionada}")
    st.markdown(f"**Ultima atualizacao:** {df_raw['datetime'].max().strftime('%d/%m/%Y %H:%M:%S')}")

    if df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
    else:
        latest = df.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Temperatura", f"{latest['temperature']:.1f} °C", 
                      delta=f"{latest['temperature'] - latest['feels_like']:.1f} °C (feels)",
                      delta_color="inverse")
        with col2:
            st.metric("Umidade", f"{latest['humidity']}%")
        with col3:
            st.metric("Vento", f"{latest['wind_speed']:.1f} m/s")
        with col4:
            st.metric("Condicao", latest['weather_main'], help=latest['weather_description'])

        st.divider()

        tab_evolucao, tab_distribuicao, tab_dados = st.tabs([
            "Evolucao Temporal", 
            "Distribuicao e Medias", 
            "Dados Brutos"
        ])

        with tab_evolucao:
            st.subheader("Variacao de Temperatura e Sensacao Termica")
            chart_data = df.set_index("datetime")[["temperature", "feels_like"]].sort_index()
            st.line_chart(chart_data)
            
            st.subheader("Variacao da Umidade (%)")
            st.area_chart(df.set_index("datetime")["humidity"].sort_index())

        with tab_distribuicao:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Frequencia de Condicoes Climaticas")
                weather_counts = df["weather_main"].value_counts()
                st.bar_chart(weather_counts)
            
            with c2:
                st.subheader("Estatisticas Rapidas")
                stats = df[["temperature", "humidity", "wind_speed"]].describe().T
                st.table(stats[["mean", "min", "max"]])

        with tab_dados:
            st.subheader("Historico de Registros")
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao acessar o banco de dados: {str(e)}")
    with st.expander("Detalhes do Erro"):
        st.write(e)
    st.info("Verifique se o container do banco está rodando e se os dados foram inseridos.")
    st.stop()
