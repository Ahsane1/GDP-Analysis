#cleans data 
def clean_data(df):
    # Removing missing values
    df = df.dropna(subset=["Value"])

    # year into int and type checking
    try:
        df["Year"] = df["Year"].map(lambda y: int(str(y).strip()))
    except Exception as e:
        raise ValueError(f"Invalid Year values found: {e}")

    # value to float
    try:
        df["Value"] = df["Value"].map(lambda v: float(v))
    except Exception as e:
        raise ValueError(f"Invalid GDP values found: {e}")

    # region into string and stripping
    df["Region"] = df["Region"].map(lambda r: str(r).strip())

    return df

#cleans config.json
def clean_config(config):

    region = config.get("region")

    if not region:
        raise ValueError("Config must include 'region'")

    if isinstance(region, str):
        regions = [region]
    else:
        raise ValueError("'region' must be a string ")

    
    try:
        year = int(config.get("year"))
    except Exception:
        raise ValueError("'year' must be a valid integer")

    
    operation = config.get("operation", "").lower()
    if operation not in {"average", "sum"}:
        raise ValueError("Operation must be 'average' or 'sum'")

    
    output = config.get("output", "dashboard").lower()

    return {
        "regions": regions,
        "year": year,
        "operation": operation,
        "output": output
    }




def filter_data(df, config):

    region = config.get("region")
    year = config.get("year")
    country = config.get("country")

    return df[
        ((df["Region"] == region) & (df["Year"] == year)) |
        (df["Country Name"] == country)
    ]

def filter_by_year(df,year):
    return list(filter(lambda x: x["Year"] == year, df))

def filter_by_region(df, region):
    return list(filter(lambda x: x["Region"] == region, df))
def filter_by_country(df, country):
    return list(filter(lambda x: x["Country Name"] == country, df))



def sum_avg_gdp_of_region(df, region, op):
    filtered = filter_by_region(df, region)
    countries = set(x["Country Name"] for x in filtered)
    avg_list = list(map(lambda c: avg_gdp_of_country(df, c), countries))
    if op == "sum":
        return sum(avg_list)
    elif op == "average":
        return sum(avg_list) / len(avg_list) if avg_list else 0
    return -1

# it might have issue check later.
# def avg_gdp_of_region(df, region): 
#     filtered = filter_by_region(df, region)
#     total = sum_avg_gdp_of_region(df, region, "sum")
#     return total / len(filtered) if filtered else 0  #error handling for division by zero

def sum_gdp_of_country(df, country):
    filtered = filter_by_country(df, country)
    return sum(x["Value"] for x in filtered)

def avg_gdp_of_country(df, country):
    filtered = filter_by_country(df, country)
    total = sum_gdp_of_country(df, country)
    return total / len(filtered) if filtered else 0  #error handling for division by zero

def filter_data_by_config(df_list, config):
    """
    Filters list of dicts based on config:
    - region
    - year
    - optional country
    Returns filtered list
    """
    filtered = df_list
    if "region" in config:
        filtered = filter_by_region(filtered, config["region"])
    if "year" in config:
        filtered = filter_by_year(filtered, config["year"])
    if "country" in config and config["country"]:
        filtered = filter_by_country(filtered, config["country"])
    return filtered



# def compute_statistics(df_list, config):
#     """
#     Compute GDP statistics based on config
#     - operation: 'sum' or 'average'
#     - target: region or country
#     """
#     operation = config.get("operation")
#     region = config.get("region")
#     country = config.get("country", None)

#     if country:  # prioritize country if given
#         if operation == "sum":
#             return sum_gdp_of_country(df_list, country)
#         elif operation == "average":
#             return avg_gdp_of_country(df_list, country)
#     else:
#         if operation == "sum":
#             return sum_gdp_of_region(df_list, region)
#         elif operation == "average":
#             return avg_gdp_of_region(df_list, region)

#     return 0  




# # ------------------ GENERAL STATISTICS ------------------
# def sum_gdp_of_country_all_years(df_list, country):
#     """Sum of GDP for a country across all years."""
#     filtered = filter_by_country(df_list, country)
#     return sum(x["Value"] for x in filtered)

# def avg_gdp_of_country_all_years(df_list, country):
#     """Average GDP for a country across all years."""
#     filtered = filter_by_country(df_list, country)
#     total = sum(x["Value"] for x in filtered)
#     return total / len(filtered) if filtered else 0

# def sum_avg_gdp_of_region_all_years(df_list, region):
#     """Sum of average GDP of all countries in a region across all years."""
#     filtered = filter_by_region(df_list, region)
#     countries = set(x["Country Name"] for x in filtered)
#     avg_list = list(map(lambda c: avg_gdp_of_country_all_years(df_list, c), countries))
#     return sum(avg_list)

# def avg_gdp_of_region_all_years(df_list, region):
#     """Average GDP of region = sum of country averages / number of countries."""
#     filtered = filter_by_region(df_list, region)
#     countries = set(x["Country Name"] for x in filtered)
#     total_sum = sum_avg_gdp_of_region_all_years(df_list, region)
#     return total_sum / len(countries) if countries else 0

