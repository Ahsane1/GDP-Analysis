import pandas as pd
import os
import json

BASE_COLUMNS = {"Country Name", "Continent"}
current_dir = os.path.dirname(os.path.abspath(__file__))
REQUIRED_CONFIG_FIELDS = {"region", "year", "operation", "output"}
DEFAULT_CONFIG_PATH = os.path.join(current_dir, "../config/config.json")
DEFAULT_DATA_PATH = os.path.join(current_dir, "../data/gdp_data.csv")


def load_config(config_path = DEFAULT_CONFIG_PATH):

    # checking if file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        raise ValueError(f"Invalid JSON format: {e}")

    missing = REQUIRED_CONFIG_FIELDS - set(config.keys())
    if missing:
        raise ValueError(f"Missing config fields: {missing}")

    return config

def load_gdp_data(file_path= DEFAULT_DATA_PATH):

    #  Check if file exists 
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    #  loading data from csv into pandas data frame 
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    #  validating the base columns
    missing_cols = BASE_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    #  renaming continent to region 
    df = df.rename(columns={"Continent": "Region"})

    # making sure there exist year columns
    year_columns = list(filter(lambda c: c.isdigit(), df.columns))
    if not year_columns:
        raise ValueError("No year columns found in dataset")

    # conversion wide format to long format
    df_long = df.melt(
        id_vars=["Country Name", "Region"],
        value_vars=year_columns,
        var_name="Year",
        value_name="Value"
    )

    return df_long

