import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Data exploration and preparation")

st.subheader("We started with data from 3 different datasets")

st.markdown("The first dataset holds information on participants in Olympic games. It holds 70.000 rows and 15 columns. "
            "The second dataset is mainly a key to convert Olympic country codes into corresponding country names (like 'GER' into 'Germany'). "
            "Both can be found on: https://www.kaggle.com/datasets/bhanupratapbiswas/olympic-data")

st.markdown("The third dataset holds demographic data. It has 234 rows and 17 columns. "
            "Can be found on: https://www.kaggle.com/datasets/tanishqdublish/world-data-population")


st.subheader("How we retrieve the data")

st.markdown("All three datasets are downloaded with the **Kaggle API** (`kagglehub.dataset_download`) in our notebook, "
            "so anyone can get exactly the same data again. The notebook then cleans and combines the datasets "
            "and saves the result as `df_usable_case2.csv`. This app reads that file, so it stays fast. "
            "Every step, with its output, can be checked in the notebook: "
            "https://github.com/JesseKnibbe/Olympic-dataset-version-1/blob/main/Olympic_workbook.ipynb")

st.markdown("**Fields we use from each dataset:**\n"
            "- *dataset_olympics.csv*: ID, Sex, Age, Height, Weight, Team, NOC, Year, Season, City, Sport, Event, Medal "
            "(the column Name is removed straight away, we do not need it)\n"
            "- *noc_region.csv*: noc_region (key) and reg (country name)\n"
            "- *world_population_data.csv*: country and the population in 1970, 1980, 1990, 2000, 2010, 2015 and 2020\n\n"
            "**Joins:** Olympic data + NOC table on the NOC code, then + population on country name and year.")


st.subheader("From raw data to a usable dataset")

url_1 = "df_usable_case2.csv"                               # read the csv straight from the repo

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

df = load_data(url_1)

steps = pd.DataFrame({
    "Step": ["Raw Olympic dataset",
             "Winter games removed",
             "Merged with NOC table (left join on NOC)",
             "Rows with missing height/weight removed",
             "Only games 1968-2016 (range of the population data)",
             "Merged with population data (left join on year + country)",
             "Unique athletes per games (one athlete, several events = 1)"],
    "Rows": [70000, 58467, 58467, 58275, 39421, len(df),
             len(df.drop_duplicates(["ID", "Year"]))],      # last two are calculated live from the csv
})
steps["Change"] = steps["Rows"].diff().fillna(0).astype(int)
st.dataframe(steps, hide_index=True)



st.subheader("Choices we made")

st.markdown(
    "- **Summer games only.** Our question is about chances to participate; winter sports depend heavily on climate, "
    "which would add a second explanation we cannot separate.\n"
    "- **Left join with the NOC table** kept every row (58.467 before and after). Missing country names "
    "(Singapore, Tuvalu, Refugee team, Unknown) were filled in by hand.\n"
    "- **192 rows dropped** because height and weight could not be filled in: the sport had no known values at all. "
    "Height and weight are not used to answer our question.\n"
    "- **1968-2016 only**, because the population data starts in 1970. For each games we estimated the population "
    "by linear interpolation between the measured years; 1968 gets the 1970 value.\n"
    "- **30 rows lost in the population merge**: 24 Individual Olympic Athletes and 6 Refugee Olympic Team. "
    "They have no country, so there is no population to compare with.\n"
    "- **Athletes are counted once per games.** 9.646 rows are the same athlete in more events. That is not an error, "
    "so we did not remove them from the data, but we count unique athletes in the analysis."
)



st.subheader("Quality checks")

col1, col2 = st.columns(2)
col1.metric("Fully duplicated rows", int(df.duplicated().sum()))
col2.metric("Same athlete, more events", int(df.duplicated(["ID", "Year"]).sum()))

st.markdown("Ranges of age, height and weight. Extremes are plausible: young gymnasts and swimmers, "
            "coxswains in rowing and heavyweight lifters.")
st.dataframe(df[["Age", "Height", "Weight"]].describe().round(1))

st.caption("Note: the Kaggle dataset is a sample of about 3.000 athletes per games, "
           "while in reality more than 10.000 take part. Shares and ratios are still comparable between years.")


st.subheader("The final dataset")
st.dataframe(df)

