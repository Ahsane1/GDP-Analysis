#cleans data 
def clean_data(df):
    # Removing missing values
    df = df.dropna(subset=["Value"])

    # Convert Year into int
    df["Year"] = df["Year"].map(lambda y: int(str(y).strip()))

    # Convert Value into float
    df["Value"] = df["Value"].map(lambda v: float(v))

    # Striping spaces from Region
    df["Region"] = df["Region"].map(lambda r: str(r).strip())

    return df

#cleans config.json
def clean_config(config):

    region = config.get("region")

    if not region:
        raise ValueError("Config must include 'region'")

    # single OR multiple regions
    if isinstance(region, str):
        regions = [region]
    elif isinstance(region, list):
        regions = region
    else:
        raise ValueError("'region' must be a string or list")

    
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




#operations 
def filter_by_region(df, region):
    return df[df["Region"] == region]

def filter_by_country(df, country):
    return df[df["Country Name"] == country]

def filter_by_year(df, year):
    return df[df["Year"] == year]



#helper fucntion for average gdp of a country
def sum_gdp_country(filtered):
    return filtered["Value"].sum()

def avg_gdp_country(df, country):
    filtered = filter_by_country(df, country)
    sum_country = sum_gdp_country(filtered)  
    return sum_country/len(filtered) if filtered else 0



#extra for now 
def sum_gpd_region(df, region):
    filtered = filter_by_region(df, region)
    return filtered["Value"].sum()


# filter by regions list  helper for avergae and sum of regions
def filter_by_regions(df, regions):
    return df[df["Region"].isin(regions)]


def sum_gdp_by_regions(df, regions):
    return (
        filter_by_regions(df, regions)["Value"]
        .sum()
    )
   
def avg_gdp_regions(df, regions):
    filtered= df[df["Region"].isin(regions)]
    sum = sum_gdp_by_regions(df, regions)
    return sum/filtered if filtered else 0




def compute_statistics(df, config):

    operation = config.get("operation").lower()

    if operation == "average":
        return df["Value"].mean()
    elif operation == "sum":
        return df["Value"].sum()
    else:
        raise ValueError(f"Invalid operation: {operation}")