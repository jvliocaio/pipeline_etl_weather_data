import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(env_path)

@st.cache_resource
def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD'))}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

@st.cache_data
def load_data():
    engine = get_engine()
    query = "SELECT * FROM weather_data"
    return pd.read_sql(query, engine)

st.title("🌤️ Weather Dashboard")

df = load_data()

st.write("Preview dos dados")
st.dataframe(df)

st.line_chart(df.set_index("datetime")["temperature"])

st.bar_chart(df["temperature"])

cidade = st.selectbox("Cidade", df["city_name"].unique())

df_filtrado = df[df["city_name"] == cidade]

st.line_chart(df_filtrado.set_index("datetime")["temperature"])

st.metric("Temperatura atual", f"{df_filtrado['temperature'].iloc[-1]} °C")
st.metric("Umidade", f"{df_filtrado['humidity'].iloc[-1]} %")
st.metric("Vento", f"{df_filtrado['wind_speed'].iloc[-1]} m/s")

