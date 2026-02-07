def clean_data(df):
   
    #Cleans GDP data , removes missing values, converting year to int and value to float 

    df = df.dropna(subset=["Value"]) # removing null value rows

    df["Year"] = df["Year"].map(lambda y: int(y)) # year to integer
    df["Value"] = df["Value"].map(lambda v: float(v)) # value to float 

    return df

def filter_data(df, config):

    region = config.get("region")
    year = config.get("year")

    filtered_df = df[
        (df["Region"] == region) &
        (df["Year"] == year)
    ]

    return filtered_df

def compute_statistics(df, config):

    operation = config.get("operation").lower()

    if operation == "average":
        return df["Value"].mean()
    elif operation == "sum":
        return df["Value"].sum()
    else:
        raise ValueError(f"Invalid operation: {operation}")