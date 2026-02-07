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


def compute_statistics(df, config):
    """
    Computes statistics based on config:
    - average
    - sum
    """

    operation = config.get("operation")

    if operation == "average":
        return df["Value"].mean()
    elif operation == "sum":
        return df["Value"].sum()
    else:
        raise ValueError("Invalid operation in config")
