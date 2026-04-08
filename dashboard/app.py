import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# LOG_DOCKER_BOOT: O script Streamlit está iniciando agora!
print("LOG_DOCKER_BOOT: O script Streamlit está iniciando agora!")

env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(env_path)

# @st.cache_resource
def get_engine():
    try:
        user = os.getenv('DB_USER')
        password = quote_plus(os.getenv('DB_PASSWORD'))
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
        
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        print(f"LOG_DOCKER_CONNECT: Tentando conectar ao banco em {host}:{port}")
        
        return create_engine(url)
    except Exception as e:
        print(f"LOG_DOCKER_ERROR: Erro ao criar engine: {e}")
        raise e

# @st.cache_data
def load_data():
    try:
        engine = get_engine()
        # Especificando o schema public explicitamente
        query = "SELECT * FROM public.sp_weather"
        print(f"LOG_DOCKER_QUERY: Executando consulta na tabela public.sp_weather")
        
        df = pd.read_sql(query, engine)
        print(f"LOG_DOCKER_SUCCESS: Dados carregados. Total: {len(df)} linhas")
        return df
    except Exception as e:
        print(f"LOG_DOCKER_ERROR: Erro ao carregar dados: {str(e)}")
        # Repassa o erro para ser tratado no bloco principal
        raise e

st.title("🌤️ Weather Dashboard")

# Exibe as configurações atuais na tela para debug (será removido depois)
# with st.expander("🛠️ Debug de Conexão"):
#     st.write(f"**Host:** `{os.getenv('DB_HOST')}`")
#     st.write(f"**Porta:** `{os.getenv('DB_PORT')}`")
#     st.write(f"**Database:** `{os.getenv('DB_NAME')}`")
#     st.write(f"**User:** `{os.getenv('DB_USER')}`")

try:
    df = load_data()
    
    st.write("Preview dos dados")
    st.dataframe(df.tail(10))

    # Gráficos
    st.subheader("📈 Evolução da Temperatura")
    st.line_chart(df.set_index("datetime")["temperature"])

    st.subheader("📊 Distribuição de Temperatura")
    st.bar_chart(df["temperature"])

    # Filtros
    cidade = st.selectbox("Selecione a Cidade", df["city_name"].unique())
    df_filtrado = df[df["city_name"] == cidade]

    if not df_filtrado.empty:
        st.line_chart(df_filtrado.set_index("datetime")["temperature"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperatura atual", f"{df_filtrado['temperature'].iloc[-1]} °C")
        col2.metric("Umidade", f"{df_filtrado['humidity'].iloc[-1]} %")
        col3.metric("Vento", f"{df_filtrado['wind_speed'].iloc[-1]} m/s")
    else:
        st.warning("Nenhum dado encontrado para a cidade selecionada.")

except Exception as e:
    st.error(f"⚠️ Erro ao acessar o banco de dados: {str(e)}")
    st.info("Verifique se o container do banco está rodando e se os dados foram inseridos.")
    st.stop()

