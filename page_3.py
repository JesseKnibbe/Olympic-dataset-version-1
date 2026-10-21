import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Hypothesis testing")

st.markdown("Our hypothesis: **over time, participation in the Olympics is becoming more equal over continents.** "
            "If that is true, the share of athletes of every continent should move towards its share of the world population.")


url_1 = "df_usable_case2.csv"                               # read the csv straight from the repo, no web address needed

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(url_1)
d_all = df.drop_duplicates(["ID", "Year"])                  # one row per athlete per games, multiple events count once

years = sorted(d_all["Year"].unique())
continents = sorted(d_all["continent_7"].unique())


# filters in the sidebar: every chart on this page reacts to them
with st.sidebar:
    st.header("Filters")
    year_range = st.select_slider("Games (from - to)", options=years, value=(years[0], years[-1]))
    chosen = st.multiselect("Continents", continents, default=continents)
    exclude_host = st.checkbox("Exclude host country", value=False,
                               help="The host country usually sends extra athletes. When ticked, the host of every games is left out.")

if not chosen:                                              # empty selection: readable message instead of an error
    st.info("Choose at least one continent in the sidebar to see the charts.")
    st.stop()

d = d_all[(d_all["Year"] >= year_range[0]) & (d_all["Year"] <= year_range[1])]
if exclude_host:
    d = d[~d["host"]]                                       # host country out of both the athletes and the population


# same calculation as in our notebook
share = pd.crosstab(d["continent_7"], d["Year"], normalize="columns") * 100     # share of athletes per continent, each year sums to 100%

pop_share = (
    d.drop_duplicates(["Year", "country_clean"])            # one row per country per games
     .groupby(["continent_7", "Year"])["pct_of_world"].sum()
     .unstack("Year")
)

ratio = share / pop_share                                   # >1 = over-represented, <1 = under-represented

# plotly wants long format: one row per continent per year
ratio_long = ratio.stack().rename("ratio").reset_index()
share_long = share.stack().rename("share").reset_index()
ratio_long = ratio_long[ratio_long["continent_7"].isin(chosen)]     # filter after calculating, so shares stay relative to the whole world
share_long = share_long[share_long["continent_7"].isin(chosen)]

st.caption(f"Selection: **{', '.join(chosen) if len(chosen) < len(continents) else 'all continents'}**, "
           f"{year_range[0]}-{year_range[1]}{', without host country' if exclude_host else ''}")


# charts
tab1, tab2 = st.tabs(["Share of athletes", "Over- and under-representation"])

with tab1:
    st.subheader("Which continents send more or fewer athletes than their population suggests?")
    fig = px.line(ratio_long, x="Year", y="ratio", color="continent_7", symbol="continent_7", markers=True,
                  log_y=True,
                  labels={"Year": "Games", "ratio": "Athlete share / population share (log)", "continent_7": "Continent"})
    fig.add_hline(y=1, line_dash="dash", line_color="grey")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Above the dashed line a continent sends more athletes than its population suggests, below it fewer. "
               "The axis is logarithmic, so 2x too many is as far from the line as 2x too few. "
               "If our hypothesis is right, the lines move towards 1 over time.")

with tab2:
    st.subheader("Share of all athletes per continent")
    fig = px.line(share_long, x="Year", y="share", color="continent_7", symbol="continent_7", markers=True,
                  labels={"Year": "Games", "share": "Share of athletes (%)", "continent_7": "Continent"})
    st.plotly_chart(fig, use_container_width=True)
    st.caption("This is the share of all athletes, without correcting for population. "
               "Compare with the first tab: a big share can still be fair if the continent has many inhabitants.")
