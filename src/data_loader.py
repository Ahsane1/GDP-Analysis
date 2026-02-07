import json
import csv
import os


current_dir = os.path.dirname(os.path.abspath(__file__))

DEFAULT_CONFIG_PATH = os.path.join(current_dir, "../config/config.json")
DEFAULT_DATA_PATH = os.path.join(current_dir, "../data/gdp_data.csv")

def load_config(config_path=None):
    
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at: {config_path}")
        return None

def load_gdp_data(csv_path=None):
    
    if csv_path is None:
        csv_path = DEFAULT_DATA_PATH

    # Check if file exists
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at: {csv_path}")
        return []

    with open(csv_path, mode="r", encoding='latin1') as f:
        reader = csv.DictReader(f)
        return list(reader)

#testing
if __name__ == "__main__":
    print(f"Script is running from: {current_dir}")
    print(f"Looking for config at: {DEFAULT_CONFIG_PATH}")
    print(f"Looking for data at:   {DEFAULT_DATA_PATH}")
    
    configg = load_config()
    print(configg)
    data = load_gdp_data()
    print(f"Rows loaded: {len(data)}")
    print(data[0])