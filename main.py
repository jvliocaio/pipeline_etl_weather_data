from src.extract_data import extract_weather_data
from src.load_data import load_weather_data
from src.transform_data import data_transformations

import os
from pathlib import Path
from dotenv import load_dotenv

import logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message )s"
)

env_path = Path(__file__).parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')

url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}'
table_name = 'sp_weather'

def pipeline():
    try:
        logging.info("Starting the weather data pipeline.")
        
        extract_weather_data(url)
        logging.info("Data extraction completed.")
        
        df = data_transformations()
        logging.info("Data transformation completed.")
        
        load_weather_data(table_name, df)
        logging.info("Data loading completed.")
        
        print("\n"+ "="*50)
        print("Weather data pipeline executed successfully!")
        print("="*50 + "\n")
    except Exception as e:  
        logging.error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        
pipeline()