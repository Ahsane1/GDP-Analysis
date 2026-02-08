
# ------------------ IMPORTS ------------------
from data_loader import load_gdp_data, load_config
from data_processer import clean_data, avg_gdp_of_country,  sum_avg_gdp_of_region
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
avg_region = sum_avg_gdp_of_region(df_list, region, "average") /1e9
sum_region = sum_avg_gdp_of_region(df_list, region, "sum")/1e9
avg_country = avg_gdp_of_country(df_list, country) /1e9

# ------------------ DASHBOARD FIGURE ------------------
fig = go.Figure()

# ------------------ KPIs ------------------
# Top row KPIs
fig.add_trace(go.Indicator(
    mode="number",
    value=avg_region,
    number={"prefix": "$", "suffix": " B", "valueformat": ",.2f", "font": {"size": 30}},
    title={"text": f"Avg GDP of {region}", "font": {"size": 20}},
    domain={'x': [0.0, 0.3], 'y': [0.85, 1]}  # top 25% of figure
))

fig.add_trace(go.Indicator(
    mode="number",
    value=sum_region,
    number={"prefix": "$", "suffix": " B", "valueformat": ",.2f", "font": {"size": 30}},
    title={"text": f"Sum GDP of {region}", "font": {"size": 20}},
    domain={'x': [0.35, 0.65], 'y': [0.85, 1]}  # top 25% of figure
))

fig.add_trace(go.Indicator(
    mode="number",
    value=avg_country,
    number={"prefix": "$", "suffix": " B", "valueformat": ",.2f", "font": {"size": 30}},
    title={"text": f"Avg GDP of {country}", "font": {"size": 20}},
    domain={'x': [0.7, 1.0], 'y': [0.85, 1]}  # top 25% of figure
))

# ------------------ LAYOUT ------------------
fig.update_layout(
    height=1600,
    width=1600,      # total figure size
    margin=dict(t=50, b=50, l=50, r=50),  # top, bottom, left, right spacing
    template="plotly_dark"  # optional, makes it look cooler
)


fig.add_annotation(
    text=f"<b>GDP DASHBOARD ({region}, {country}, {year})</b>",
    x=0.5, y=1.0, xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=28),
    align="center"
)
# ------------------ PIE CHART ------------------
from data_processer import filter_by_year, filter_by_region

# Filter data by year
year_filtered = filter_by_year(df_list, year)

# Filter data by region
region_filtered = filter_by_region(year_filtered, region)

# Prepare data
pie_countries = [x["Country Name"] for x in region_filtered]
pie_values = [x["Value"] / 1e9 for x in region_filtered]  # convert to billions

# Add pie chart to figure (bottom-left)
fig.add_annotation(
    text=f"GDP Distribution in {region} ({year})",
    x=0.06, y=0.3,  # adjust position above pie chart
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=20, color="white"),
    align="center"
)
fig.add_trace(go.Pie(
    labels=pie_countries,
    values=pie_values,
    showlegend=False,
    textinfo="none",
   # title=f"GDP Distribution in {region} ({year})",
    hovertemplate="%{label}: $%{value:,.2f} B<br>%{percent}",  # hover info
    name=f"GDP Distribution ({year})",
    domain={'x': [0, 0.25], 'y': [0, 0.25]}  # correct bottom-left
))





# ------------------ BAR CHART ------------------
# Same data as Pie (year & region filtered)
bar_countries = pie_countries
bar_values = pie_values  # already in billions

# Add annotation (title for bar chart)
fig.add_annotation(
    text=f"GDP by Country in {region} ({year})",
    x=0.7, y=0.45,  # top-center of bar chart area
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=20, color="white"),
    align="center"
)

# Add Bar chart
fig.add_trace(go.Bar(
    x=bar_countries,
    y=bar_values,
    marker_color="orange",
    name=f"GDP by Country ({year})",
    hovertemplate="%{x}: $%{y:,.2f} B"
), 
# position in figure using domain (bottom-right)
row=None, col=None  # domain controls position
)

# Use domain to position the Bar chart
fig.update_traces(
    selector=dict(type='bar'),
    xaxis="x2",
    yaxis="y2"
)

# Create extra axes for bar chart in layout
fig.update_layout(
    xaxis2=dict(domain=[0.55, 0.95]),   # horizontal position
    yaxis2=dict(domain=[0, 0.4]),       # vertical position (bottom-right)
)

#---------------- SAVE & OPEN ------------------
fig.write_html("dashboard.html")
webbrowser.open("dashboard.html")

