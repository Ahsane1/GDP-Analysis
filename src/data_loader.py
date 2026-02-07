import pandas as pd
import os

BASE_COLUMNS = {"Country Name", "Continent"}
current_dir = os.path.dirname(os.path.abspath(__file__))

DEFAULT_CONFIG_PATH = os.path.join(current_dir, "../config/config.json")
DEFAULT_DATA_PATH = os.path.join(current_dir, "../data/gdp_data.csv")

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
data = load_gdp_data()
print(data.head())
print(data.columns)