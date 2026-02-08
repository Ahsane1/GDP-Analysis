# ------------------ IMPORTS ------------------
from data_loader import load_gdp_data, load_config
from data_processer import clean_data, avg_gdp_of_country, sum_avg_gdp_of_region
from data_processer import filter_by_year, filter_by_region, filter_by_country
import plotly.graph_objects as go
import webbrowser

# ------------------ LOAD CONFIG & DATA ------------------
config = load_config()
df = load_gdp_data()
df = clean_data(df)
df_list = df.to_dict("records")

region = config["region"]
country = config.get("country")
year = config["year"]

# ------------------ KPI VALUES ------------------
avg_region = sum_avg_gdp_of_region(df_list, region, "average") / 1e9
sum_region = sum_avg_gdp_of_region(df_list, region, "sum") / 1e9
avg_country = avg_gdp_of_country(df_list, country) / 1e9

# ------------------ FIGURE ------------------
fig = go.Figure()

# ------------------ TOP KPIs ------------------
# fig.add_trace(go.Indicator(
#     mode="number",
#     value=avg_region,
#     number={"prefix": "$", "suffix": " B", "valueformat": ",.2f", "font": {"size": 30}},
#     title={"text": f"Avg GDP of {region}", "font": {"size": 20}},
#     domain={'x': [0, 0.3], 'y': [0.9, 1]}
# ))
# fig.add_trace(go.Indicator(
#     mode="number",
#     value=sum_region,
#     number={"prefix": "$", "suffix": " B", "valueformat": ",.2f", "font": {"size": 30}},
#     title={"text": f"Sum GDP of {region}", "font": {"size": 20}},
#     domain={'x': [0.35, 0.65], 'y': [0.9, 1]}
# ))
# fig.add_trace(go.Indicator(
#     mode="number",
#     value=avg_country,
#     number={"prefix": "$", "suffix": " B", "valueformat": ",.2f", "font": {"size": 30}},
#     title={"text": f"Avg GDP of {country}", "font": {"size": 20}},
#     domain={'x': [0.7, 1], 'y': [0.9, 1]}
# ))

# ------------------ KPI BOX STYLE ------------------
KPI_BOX = dict(
    type="rect",
    xref="paper",
    yref="paper",
    fillcolor="rgba(0,0,0,0.45)",
    line=dict(color="white", width=1),
    layer="below"
)

# ------------------ KPI 1 : AVG REGION ------------------
fig.add_shape(**KPI_BOX, x0=0.00, x1=0.30, y0=0.8, y1=0.9)
fig.add_trace(go.Indicator(
    mode="number",
    value=avg_region,
    number=dict(prefix="$", suffix=" B", valueformat=",.2f",
                font=dict(size=30, color="white")),
    title=dict(text=f"Avg GDP of {region}",
               font=dict(size=18, color="white")),
    domain=dict(x=[0.00, 0.30], y=[0.8, 0.900])
))

# ------------------ KPI 2 : SUM REGION ------------------
fig.add_shape(**KPI_BOX, x0=0.35, x1=0.65, y0=0.8, y1=0.9)
fig.add_trace(go.Indicator(
    mode="number",
    value=sum_region,
    number=dict(prefix="$", suffix=" B", valueformat=",.2f",
                font=dict(size=30, color="white")),
    title=dict(text=f"Sum GDP of {region}",
               font=dict(size=18, color="white")),
    domain=dict(x=[0.35, 0.65], y=[0.8, 0.900])
))

# ------------------ KPI 3 : AVG COUNTRY ------------------
fig.add_shape(**KPI_BOX, x0=0.70, x1=1.00, y0=0.8, y1=0.9)
fig.add_trace(go.Indicator(
    mode="number",
    value=avg_country,
    number=dict(prefix="$", suffix=" B", valueformat=",.2f",
                font=dict(size=30, color="white")),
    title=dict(text=f"Avg GDP of {country}",
               font=dict(size=18, color="white")),
    domain=dict(x=[0.70, 1.00],y=[0.8, 0.900])
))
# ---------------------Head Title----------------------
fig.add_annotation(
    text=f"<b>GDP DASHBOARD ({region}, {country}, {year})</b>",
    x=0.5,
    y=1.02,
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=28),
    align="center"
)

# ------------------ LINE CHART (full width) ------------------
country_filtered = filter_by_country(df_list, country)
country_filtered.sort(key=lambda x: x["Year"])
line_years = [x["Year"] for x in country_filtered]
line_values = [x["Value"] / 1e9 for x in country_filtered]\


# -------- LINE CHART TITLE --------
fig.add_annotation(
    text=f"GDP Progress of {country} Over Years",
    x=0.5,
    y=0.765,
    xref="paper",
    yref="paper",
    showarrow=False,

    font=dict(
        size=20,
        color="white"
    ),
    align="center",

    # visual polish
    bgcolor="rgba(0,0,0,0.45)",
    bordercolor="white",
    borderwidth=1,
    borderpad=8,
    opacity=0.95
)

# -------- LINE CHART --------
fig.add_trace(go.Scatter(
    x=line_years,
    y=line_values,
    mode="lines+markers",

    line=dict(
        color="lightgreen",
        width=3
    ),
    marker=dict(
        size=7,
        color="lightgreen",
        line=dict(color="white", width=1)
    ),

    hovertemplate=(
        "<b>Year %{x}</b><br>"
        "GDP: $%{y:,.2f} B<extra></extra>"
    ),

    showlegend=False
))

# -------- AXES & POSITIONING --------
fig.update_layout(
    xaxis=dict(
        domain=[0.05, 0.95],
        anchor="y",
        showgrid=False,
        tickfont=dict(size=11, color="white"),
        title=dict(
            text="Year",
            font=dict(size=12, color="white")
        )
    ),
    yaxis=dict(
        domain=[0.60, 0.72],
        anchor="x",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)",
        tickfont=dict(size=11, color="white"),
        title=dict(
            text="GDP (Billion $)",
            font=dict(size=12, color="white")
        )
    )
)

# -------- LINK TRACE TO AXES --------
fig.update_traces(
    selector=dict(type='scatter'),
    xaxis="x",
    yaxis="y"
)

# ------------------ PIE CHART (bottom-left) ------------------
year_filtered = filter_by_year(df_list, year)
region_filtered = filter_by_region(year_filtered, region)
pie_countries = [x["Country Name"] for x in region_filtered]
pie_values = [x["Value"] / 1e9 for x in region_filtered]

fig.add_annotation(
    text=f"GDP Distribution in {region} ({year})",
    x=0.045,
    y=0.260,
    xref="paper",
    yref="paper",
    showarrow=False,

    font=dict(
        size=18,
        color="white"
    ),
    align="center",

    # makes heading readable
    bgcolor="rgba(0,0,0,0.4)",
    bordercolor="white",
    borderwidth=1,
    borderpad=5,
    opacity=0.95
)

fig.add_trace(go.Pie(
    labels=pie_countries,
    values=pie_values,

    # text control
    textinfo="percent",
    textposition="inside",
    textfont=dict(size=11, color="white"),

    # styling
    hole=0.0,   # keep 0 for pie (change to 0.3+ for donut)
    pull=[0.04] * len(pie_countries),
    marker=dict(
        line=dict(color="white", width=1)
    ),

    # hover
    hovertemplate=(
        "<b>%{label}</b><br>"
        "GDP: $%{value:,.2f} B<br>"
        "Share: %{percent}<extra></extra>"
    ),

    showlegend=False,
    name=f"GDP Distribution ({year})",

    domain={'x': [0.0, 0.28], 'y': [0.0, 0.25]}
))


# ------------------ BAR CHART (bottom-right) ------------------
bar_countries = pie_countries
bar_values = pie_values
# -------- BAR CHART TITLE --------
fig.add_annotation(
    text=f"GDP by Country in {region} ({year})",
    x=0.85,
    y=0.5,
    xref="paper",
    yref="paper",
    showarrow=False,

    font=dict(
        size=18,
        color="white"
    ),
    align="center",

    # visual polish
    bgcolor="rgba(0,0,0,0.4)",
    bordercolor="white",
    borderwidth=1,
    borderpad=6,
    opacity=0.95
)

# -------- BAR CHART --------
fig.add_trace(go.Bar(
    x=bar_countries,
    y=bar_values,

    marker=dict(
        color="lightsalmon",
        line=dict(color="white", width=1.2)
    ),

    hovertemplate=(
        "<b>%{x}</b><br>"
        "GDP: $%{y:,.2f} B<extra></extra>"
    ),

    showlegend=False
))

# -------- AXES & POSITIONING --------
fig.update_layout(
    xaxis2=dict(
        domain=[0.55, 0.95],
        anchor="y2",
        tickangle=-35,
        showgrid=False,
        tickfont=dict(size=11, color="white"),
        title=dict(
            text="Countries",
            font=dict(size=12, color="white")
        )
    ),
    yaxis2=dict(
        domain=[0.15, 0.45],
        anchor="x2",
        showgrid=True,
        gridcolor="rgba(255,255,255,0.15)",
        tickfont=dict(size=11, color="white"),
        title=dict(
            text="GDP (Billion $)",
            font=dict(size=12, color="white")
        )
    ),
    bargap=0.25   # space between bars
)

# -------- LINK TRACE TO AXES --------
fig.update_traces(
    selector=dict(type='bar'),
    xaxis="x2",
    yaxis="y2"
)

# ------------------ DONUT CHART ------------------
from data_processer import filter_by_year

# Filter data by selected year
year_filtered = filter_by_year(df_list, year)

# Get unique regions and their total GDP
regions = list(set([x["Region"] for x in year_filtered]))
region_values = []

for r in regions:
    total = sum([x["Value"] for x in year_filtered if x["Region"] == r])
    region_values.append(total / 1e9)  # convert to billions

# Add annotation (title for donut chart)
fig.add_annotation(
    text=f"GDP Distribution by Region ({year})",
    x=0.0275,
    y=0.560,
    xref="paper",
    yref="paper",
    showarrow=False,

    # text styling
    font=dict(
        size=20,
        color="white",
        family="Arial"
    ),

    align="center",

    # background & padding (VERY useful)
    bgcolor="rgba(0,0,0,0.4)",
    bordercolor="white",
    borderwidth=1,
    borderpad=6,

    # rotation (optional)
    textangle=0,

    # opacity
    opacity=0.9
)


# Add Donut chart
fig.add_trace(go.Pie(
    labels=regions,
    values=region_values,

    hole=0.4,        # donut size (0.3–0.6 is sweet spot)

    # text control
    textinfo="percent",
    textposition="inside",
    textfont=dict(size=12, color="white"),

    # slice styling
    pull=[0.05]*len(regions),   # small pop-out effect
    marker=dict(
        line=dict(color="white", width=1)
    ),

    # hover
    hovertemplate=(
        "<b>%{label}</b><br>"
        "GDP: $%{value:,.2f} B<br>"
        "Share: %{percent}<extra></extra>"
    ),

    showlegend=False,
    name=f"GDP by Region ({year})",

    domain={'x': [0.0, 0.28], 'y': [0.27, 0.55]}
))






# ------------------ FINAL LAYOUT ------------------
fig.update_layout(height=1800, width=1600, margin=dict(t=100, b=50, l=50, r=50), template="plotly_dark")

# ------------------ SAVE & OPEN ------------------
fig.write_html("dashboard.html")
webbrowser.open("dashboard.html")
