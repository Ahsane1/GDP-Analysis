from data_loader import load_gdp_data, load_config
from data_processer import clean_data, filter_data, compute_statistics

config = load_config()
df = load_gdp_data()
df = clean_data(df)

filtered = filter_data(df, config)

result = compute_statistics(filtered, config)

print(f"Config: {config}")
print(f"Result: {result}")
