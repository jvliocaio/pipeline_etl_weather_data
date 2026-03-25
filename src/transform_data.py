import pandas as pd
from pathlib import Path
import json

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

path_name = Path(__file__).parent.parent / "data" / "weather_data.json"

colums_names_to_drop = ["weather", "weather_icon", "sys.type"]

columns_names_to_rename = {
    "base": "base",
    "visibility": "visibility",
    "dt": "datetime",
    "timezone": "timezone",
    "id": "city_id",
    "name": "city_name",
    "cod": "code",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.type": "sys_type",
    "sys.id": "sys_id",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset",
}

columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_dataframe(path_name: str) -> pd.DataFrame:

    logging.info(f"Creating dataframe from file: {path_name}")
    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f"Dataframe created with shape: {df.shape}")
    return df


def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:

    df_weather = pd.json_normalize(df["weather"].apply(lambda x: x[0]))

    df_weather = df_weather.rename(
        columns={
            "id": "weather_id",
            "main": "weather_main",
            "description": "weather_description",
            "icon": "weather_icon",
        }
    )

    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"Column 'weather' normalized - {len(df_weather.columns)} columns")
    return df


def drop_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info(f"Dropping columns {columns_name}")
    df = df.drop(columns=columns_name)
    logging.info(f"Columns {columns_name} dropped - {df.shape[1]} columns left")
    return df


def rename_columns(df: pd.DataFrame, columns_name: dict[str, str]) -> pd.DataFrame:
    logging.info(f"Renaming columns {columns_name}")
    df = df.rename(columns=columns_name)
    logging.info(f"Columns renamed")
    return df


def normalize_datetime_columns(df: pd.DataFrame, columns_name: list[str]) -> pd.DataFrame:
    logging.info(f"Normalizing datetime columns {columns_name}")
    for name in columns_name:
        df[name] = pd.to_datetime(df[name], unit="s", utc=True).dt.tz_convert("America/Sao_Paulo")
    logging.info(f"Datetime columns normalized")
    return df

def data_transformations():
    print("Starting transformation")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, colums_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info(f"Dataframe transformed")
    return df