import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# brainstorm about layout:                                # ik werk eigenlijk uit gewoonte in het engels. Overschakelen naar Nederlands? Maar onze data is ook Engels.. Wat denk je van het echte werk in het engels en opmerkingen voor elkaar tussendoor of brainstormen zoals hieronder in het Nederlands?
# Make the tab for page 1 be "introduction"                 # Wat heeft ons aan het werk gezet, in een mooie layout
# Make the tab for page 2 be "data preparation"            # Welke data hebben we gebruikt, verantwoording van keuzes, wat hebben we ermee gedaan om aan de slag te kunnen
# Make the tab for page 3 be "analysis"                    # Beantwoorden van onze hoofdvraag en overige interessante conclusies uit de data
# Make the tab for page 4 be "conclusion"                # conclusie en uitvloeiende vragen die overblijven
                                                            # ik denk dat 4 pagina's uiteindelijk mooi gaat zijn, maar is maar een opzet...

st.title("Case 2 presentation")

st.header("Driving question:")

st.subheader("From our dataset we noticed that inhabitants of different countries or continents do not have equal chances to participate in the Olympic games.")

# <- NEW: intro figure, replaces the placeholder text
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data("df_usable_case2.csv")
d16 = df[df["Year"] == 2016].drop_duplicates(["ID", "Year"])           # Rio 2016, one row per athlete

athletes = d16["continent_7"].value_counts(normalize=True) * 100       # share of all athletes per continent
population = d16.drop_duplicates("country_clean").groupby("continent_7")["pct_of_world"].sum()   # share of world population

compare = pd.DataFrame({"Share of athletes": athletes, "Share of world population": population}).reset_index(names="Continent")
compare_long = compare.melt(id_vars="Continent", var_name="Measure", value_name="Percentage")

fig = px.bar(compare_long, x="Continent", y="Percentage", color="Measure", barmode="group",
             pattern_shape="Measure", text_auto=".0f",
             labels={"Percentage": "% of total"})
fig.update_layout(title="Rio 2016: share of athletes vs share of world population")
st.plotly_chart(fig, use_container_width=True)

asia = compare.set_index("Continent").loc["Asia"]
st.caption(f"In 2016 Asia was home to {asia['Share of world population']:.0f}% of the world population, "
           f"but sent only {asia['Share of athletes']:.0f}% of the athletes. "
           "In this presentation we look at whether this gap has become smaller over time.")




st.header("Hypothesis:")

st.subheader("Over time, participation in the Olympics is becoming more equal over countries or continents")


# ik denk dat deze naar pagina 2 moet.
data = [
    (2016, "Rio de Janeiro", -22.9068,  -43.1729),
    (2000, "Sydney",         -33.8688,  151.2093),
    (1996, "Atlanta",         33.7490,  -84.3880),
    (2008, "Beijing",         39.9042,  116.4074),
    (2004, "Athens",          37.9838,   23.7275),
    (2012, "London",          51.5074,   -0.1278),
    (1992, "Barcelona",       41.3874,    2.1686),
    (1988, "Seoul",           37.5665,  126.9780),
    (1972, "Munich",          48.1351,   11.5820),
    (1984, "Los Angeles",     34.0522, -118.2437),
    (1976, "Montreal",        45.5017,  -73.5673),
    (1968, "Mexico City",     19.4326,  -99.1332),
    (1980, "Moscow",          55.7558,   37.6173),
]

df_world = pd.DataFrame(data, columns=["year", "city", "lat", "lon"]).sort_values("year")
df_world["label"] = df_world["year"].astype(str) + " " + df_world["city"]

fig = px.scatter_geo(
    df_world,
    lat="lat",
    lon="lon",
    text="label",
    hover_name="city",
    hover_data={"year": True, "lat": False, "lon": False, "label": False},
    color="year",
    color_continuous_scale="Viridis",
    projection="natural earth",
)

fig.update_traces(
    marker=dict(size=10, line=dict(width=1.0, color="black")),
    textfont=dict(size=10, color="black"),
    textposition="top center",
)
fig.update_geos(showcountries=True, showland=True, landcolor="rgb(235,235,235)")
fig.update_layout(title="Olympic host cities 1968–2016", margin=dict(l=0, r=0, t=40, b=0))

st.plotly_chart(fig)
