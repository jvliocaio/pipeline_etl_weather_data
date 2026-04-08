from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
def get_engine():
    logging
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    )

engine = get_engine()

def load_weather_data(table_name:str, df):
    # Evitar duplicados baseados no datetime antes de inserir
    try:
        query = text(f"SELECT datetime FROM {table_name}")
        existing_times = pd.read_sql_query(query, con=engine)['datetime']
        df = df[~df['datetime'].isin(existing_times)]
        
        if df.empty:
            logging.info("Nenhum dado novo para inserir (registro duplicado).")
            return
    except Exception as e:
        logging.warning(f"Não foi possível verificar duplicados (tabela pode não existir): {e}")

    df.to_sql(name=table_name, con=engine, if_exists="append", index=False) 
    logging.info(f"Foram inseridos {len(df)} novos registros em {table_name}.")
    