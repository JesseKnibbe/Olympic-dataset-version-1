import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# url_1 = "https://raw.githubusercontent.com/jurre-m/Olympic-dataset-version-1/refs/heads/main/df_usable_case2.csv"      # if this page just activates the main page/2nd/3rd page then this dataframe doesn't need to be here probably

# df = pd.read_csv(url_1)

# Define the pages
introduction = st.Page("main_page.py", title="Introduction", icon="🎈")
hypothesis = st.Page("page_2.py", title="Data Preparation", icon="❄️")
answer = st.Page("page_3.py", title="Hypothesis Testing", icon="🎉")
conclusion = st.Page("page_4.py", title="Conclusion", icon="🏁") 

# Set up navigation
pg = st.navigation([introduction, hypothesis, answer, conclusion])

# Run the selected page
pg.run()

