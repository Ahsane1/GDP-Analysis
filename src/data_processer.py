def clean_data(df):
   
    #Cleans GDP data , removes missing values, converting year to int and value to float 

    df = df.dropna(subset=["Value"]) # removing null value rows

    df["Year"] = df["Year"].map(lambda y: int(y)) # year to integer
    df["Value"] = df["Value"].map(lambda v: float(v)) # value to float 

    return df

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


def sum_avg_gdp_of_region(df, region): #taking the sum of average GDP of countries in the region.
   
    filtered = filter_by_region(df, region)
    countries = set(x["Country Name"] for x in filtered)
    avg_list = list(map(lambda c: avg_gdp_of_country(df, c), countries))
    return sum(avg_list)

# it might have issue check later.
def avg_gdp_of_region(df, region): 
    filtered = filter_by_region(df, region)
    total = sum_avg_gdp_of_region(df, region)
    return total / len(filtered) if filtered else 0  #error handling for division by zero

def sum_gdp_of_country(df, country):
    filtered = filter_by_country(df, country)
    return sum(x["Values"] for x in filtered)

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



def compute_statistics(df_list, config):
    """
    Compute GDP statistics based on config
    - operation: 'sum' or 'average'
    - target: region or country
    """
    operation = config.get("operation")
    region = config.get("region")
    country = config.get("country", None)

    if country:  # prioritize country if given
        if operation == "sum":
            return sum_gdp_of_country(df_list, country)
        elif operation == "average":
            return avg_gdp_of_country(df_list, country)
    else:
        if operation == "sum":
            return sum_gdp_of_region(df_list, region)
        elif operation == "average":
            return avg_gdp_of_region(df_list, region)

    return 0  
