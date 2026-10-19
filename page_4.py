import streamlit as st
import pandas as pd
import numpy as np

st.title("Conclusion")


# same data and calculations as on the hypothesis page, so the numbers below always match
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data("df_usable_case2.csv")
d = df.drop_duplicates(["ID", "Year"])                      # one row per athlete per games
first, last = d["Year"].min(), d["Year"].max()

share = pd.crosstab(d["continent_7"], d["Year"], normalize="columns") * 100
pop_share = (d.drop_duplicates(["Year", "country_clean"])
              .groupby(["continent_7", "Year"])["pct_of_world"].sum()
              .unstack("Year"))
ratio = share / pop_share                                   # >1 = over-represented, <1 = under-represented

def country_table(data):
    t = (data.groupby(["Year", "country_clean"])
             .agg(athletes=("ID", "size"), pct_of_world=("pct_of_world", "first"))
             .reset_index())
    t["rate"] = t["athletes"] / t["pct_of_world"]
    return t

def gini(t):
    t = t.sort_values("rate")
    x = np.concatenate([[0], t["pct_of_world"].cumsum() / t["pct_of_world"].sum()])
    y = np.concatenate([[0], t["athletes"].cumsum() / t["athletes"].sum()])
    return 1 - np.sum((x[1:] - x[:-1]) * (y[1:] + y[:-1]))

g_with = {y: gini(t) for y, t in country_table(d).groupby("Year")}
g_without = {y: gini(t) for y, t in country_table(d[~d["host"]]).groupby("Year")}


# the answer
st.header("Is participation becoming more equal?")
st.subheader("Only a little. The gap between continents is getting smaller, but the chance per inhabitant is not.")

col1, col2, col3 = st.columns(3)
col1.metric(f"Gini {first}", f"{g_with[first]:.2f}")
col2.metric(f"Gini {last}", f"{g_with[last]:.2f}", f"{g_with[last] - g_with[first]:+.2f}", delta_color="inverse")
col3.metric(f"Ratio Asia {last}", f"{ratio.loc['Asia', last]:.2f}",
            f"{ratio.loc['Asia', last] - ratio.loc['Asia', first]:+.2f} since {first}")


# what we found, step by step
st.header("What we found")

st.markdown(
    f"1. **Africa and Asia send a bigger part of the athletes than before.** "
    f"Africa went from {share.loc['Africa', first]:.0f}% to {share.loc['Africa', last]:.0f}% of all athletes, "
    f"Asia from {share.loc['Asia', first]:.0f}% to {share.loc['Asia', last]:.0f}%. "
    f"Europe went down from {share.loc['Europe', first]:.0f}% to {share.loc['Europe', last]:.0f}%.\n"
    f"2. **Compared to their population, the differences are still very large.** "
    f"In {last} Asia sent {ratio.loc['Asia', last]:.2f} times the athletes its population suggests, "
    f"Europe {ratio.loc['Europe', last]:.1f} times and Oceania {ratio.loc['Oceania', last]:.0f} times.\n"
    f"3. **The inequality per inhabitant hardly changed.** The Gini coefficient was {g_with[first]:.2f} in {first} "
    f"and {g_with[last]:.2f} in {last}. More countries take part, but the chance for one inhabitant "
    f"is still very different depending on where you live.\n"
    f"4. **The big jumps are political, not a trend.** The boycotts of 1976, 1980 and 1984 cause the largest changes "
    f"in a single games. After each boycott the shares return to their old level."
)


# alternative explanation
st.header("Could the host country explain this?")
st.markdown(
    f"The host country always sends extra athletes, for example Brazil in {last}. "
    f"When we leave the host country out, the Gini is {g_without[first]:.2f} in {first} and {g_without[last]:.2f} in {last}: "
    "almost the same as with the host country. So the host country does **not** explain the inequality."
)


# answer to the hypothesis
st.header("Our hypothesis")
st.markdown(
    "*Over time, participation in the Olympics is becoming more equal over countries or continents.*\n\n"
    "We **partly reject** this hypothesis. The share of athletes is moving slowly towards the continents with "
    "more inhabitants, but the chance per inhabitant to take part is as unequal in 2016 as it was in 1968."
)


# limitations: what the reader should keep in mind
st.header("Limitations")
st.markdown(
    "- The Kaggle dataset is a **sample** of about 3.000 athletes per games, the real number is more than 10.000.\n"
    "- The population is **estimated** between the measured years (linear interpolation); 1968 uses the 1970 value.\n"
    "- Only **countries that took part** are counted. Countries without athletes, which had no chance at all, are not in the data.\n"
    "- Historical countries are linked to their current country (for example the Soviet Union to Russia, West and East Germany to Germany)."
)


# questions that remain
st.header("Questions that remain")
st.markdown(
    "- Does the **wealth** of a country (GDP per inhabitant) explain more than its continent?\n"
    "- Is the inequality the same for **women and men**?\n"
    "- Do the results change with the **full dataset** instead of a sample?"
)
