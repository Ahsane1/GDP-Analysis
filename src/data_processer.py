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


def filter_data(df, config):

    config["year"] = int(config["year"])
    region = config.get("region")

    filtered_df = df[
    ((df["Region"].map(lambda r: r.lower())) == region.lower()) &
    ((df["Year"]) == config["year"])
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