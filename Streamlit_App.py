
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import numpy as np
from PIL import Image

df = pd.read_csv("REBECCA.csv")


st.markdown(
    """
    <style>
    /* Full-page animated gradient background */
    .stApp {
        background: linear-gradient(270deg, #ff00cc, #3333ff, #00ffcc, #ffcc00);
        background-size: 800% 800%;
        animation: gradientShift 20s ease infinite;
        overflow: hidden;
    }

    @keyframes gradientShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(270deg, #00ffcc, #ffcc00, #ff00cc, #3333ff);
        background-size: 600% 600%;
        animation: gradientShift 15s ease infinite;
        color: white; /* text color */
    }

    /* Floating particles */
    .particle {
        position: fixed;
        width: 10px;
        height: 10px;
        background: rgba(255,255,255,0.8);
        border-radius: 50%;
        animation: floatUp 10s linear infinite;
    }

    @keyframes floatUp {
        from {transform: translateY(100vh);}
        to {transform: translateY(-10vh);}
    }

    /* Neon glow overlay */
    .neon {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        box-shadow: inset 0 0 200px rgba(255,255,255,0.2);
        pointer-events: none;
    }
    </style>

    <div class="neon"></div>
    <div class="particle" style="left:20%; animation-delay:0s;"></div>
    <div class="particle" style="left:40%; animation-delay:2s;"></div>
    <div class="particle" style="left:60%; animation-delay:4s;"></div>
    <div class="particle" style="left:80%; animation-delay:6s;"></div>
    """,
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="My Insane Streamlit App",   # Title shown in browser tab
    page_icon="🚀",                         # Emoji or image as favicon
    layout="wide",                          # Options: "centered" or "wide"
    initial_sidebar_state="expanded"        # Options: "expanded" or "collapsed"
)


st.title("Incidents Analysis Dashboard")
columns = ["Identifier","Incident","State","Start date","End date","Number of deaths"]
df = df[columns]
with st.expander("Click to check Incident Table", expanded=False):
    st.dataframe(df, width="stretch", height=200)

# Sidebar filters
# Sidebar filters (always define them first)
selected_state = st.sidebar.multiselect("Choose a State:", df["State"].unique())
selected_deaths = st.sidebar.multiselect("Choose Number of deaths:", df["Number of deaths"].unique())
selected_incident = st.sidebar.multiselect("Choose an Incident:", df["Incident"].unique())
selected_Start = st.sidebar.multiselect("Choose from Start date:", df["Start date"].unique())
selected_End = st.sidebar.multiselect("Choose from End date:", df["End date"].unique())

# Start with full dataframe
filtered_df = df.copy()

# Apply filters safely
if selected_state:
    filtered_df = filtered_df[filtered_df["State"].isin(selected_state)]

if selected_deaths:
    filtered_df = filtered_df[filtered_df["Number of deaths"].isin(selected_deaths)]

if selected_incident:
    filtered_df = filtered_df[filtered_df["Incident"].isin(selected_incident)]

if selected_Start:
    filtered_df = filtered_df[filtered_df["Start date"].isin(selected_Start)]

if selected_End:
    filtered_df = filtered_df[filtered_df["End date"].isin(selected_End)]

# Chart linked to filters




####
# Load your dataset
df = pd.read_csv("REBECCA.csv")
if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(16,6))  # wider figure
    sns.barplot(data=filtered_df, x="State", y="Number of deaths", ci=None, palette="magma", ax=ax)
    ax.set_title("Deaths by State (Filtered)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)

    # Dynamic summary
    state_deaths = filtered_df.groupby("State", as_index=False)["Number of deaths"].sum()
    top_states = state_deaths.nlargest(min(3, len(state_deaths)), "Number of deaths")

    if len(top_states) >= 3:
        summary = (
            f"This chart reflects the filtered selection. "
            f"{top_states.iloc[0]['State']} recorded the highest fatalities, "
            f"followed by {top_states.iloc[1]['State']} and {top_states.iloc[2]['State']}."
        )
    elif len(top_states) == 2:
        summary = (
            f"This chart reflects the filtered selection. "
            f"{top_states.iloc[0]['State']} recorded the highest fatalities, "
            f"followed by {top_states.iloc[1]['State']}."
        )
    elif len(top_states) == 1:
        summary = f"This chart reflects the filtered selection. {top_states.iloc[0]['State']} recorded the highest fatalities."
    else:
        summary = "No states available after filtering."

    st.write(summary)
else:
    st.write("No data matches the current filter selection.")



###q2
filtered_df["Start date"] = pd.to_datetime(filtered_df["Start date"], errors="coerce")
filtered_df["End date"] = pd.to_datetime(filtered_df["End date"], errors="coerce")

# Extract year from Start date
filtered_df["Year"] = filtered_df["Start date"].dt.year

# Chart linked to filters
if not filtered_df.empty:
    fig, ax = plt.subplots()
    filtered_df["Year"].value_counts().sort_index().plot(ax=ax, kind="line", marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Incidents")
    ax.set_title("Trend of Incidents Over Time (Filtered)")
    st.pyplot(fig)

    # Dynamic summary
    year_counts = filtered_df["Year"].value_counts().sort_index()
    if not year_counts.empty:
        top_years = year_counts.nlargest(min(3, len(year_counts)))
        summary = (
            f"This chart reflects the filtered selection. "
            f"The year {top_years.index[0]} recorded the highest number of incidents, "
            f"followed by {top_years.index[1]} and {top_years.index[2]}." 
            if len(top_years) >= 3 else
            f"This chart reflects the filtered selection. The year {top_years.index[0]} recorded the highest number of incidents."
        )
        st.write(summary)
else:
    st.write("No data matches the current filter selection.")


##q3
st.subheader("3. Are there seasonal patterns in incidents?")
df["Month"] = df["Start date"].dt.month
fig, ax = plt.subplots()
sns.countplot(data=df, x="Month", ax=ax)
st.pyplot(fig)

# Add summary
monthly_counts = df["Month"].value_counts().sort_index()
peak_month = monthly_counts.idxmax()
low_month = monthly_counts.idxmin()

st.write(
    f"Incidents show clear seasonal variation. The highest number of incidents occurs in month {peak_month}, "
    f"while the lowest occurs in month {low_month}. This suggests that certain times of the year are more prone to incidents."
)








##q5
st.subheader("5. Which incidents had the highest fatalities?")

# Select top 10 incidents by fatalities
top_incidents = df.nlargest(10, "Number of deaths")

# Plot bar chart
fig, ax = plt.subplots()
sns.barplot(data=top_incidents, x="Identifier", y="Number of deaths", ax=ax)
ax.set_title("Top 10 Incidents by Fatalities")

# Rotate labels if identifiers are tight
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")

st.pyplot(fig)

# Add summary beneath chart
summary = (
    f"This chart highlights the ten incidents with the highest recorded fatalities. "
    f"The deadliest incident was Identifier {top_incidents.iloc[0]['Identifier']} "
    f"with {top_incidents.iloc[0]['Number of deaths']} deaths, "
    f"followed by Identifier {top_incidents.iloc[1]['Identifier']} "
    f"and Identifier {top_incidents.iloc[2]['Identifier']}. "
    "These extreme cases stand out compared to the rest of the dataset, "
    "showing which individual incidents had the most severe impact."
)
st.write(summary)



##q6
st.subheader("6. How do incidents vary by top 10 state?")

# Count incidents per state
state_counts = df["State"].value_counts().reset_index()
state_counts.columns = ["State", "Count"]

# Select top 10 states with most incidents
top_states = state_counts.nlargest(10, "Count")["State"]

# Filter original dataframe to only those top 10 states
df_top_states = df[df["State"].isin(top_states)]

# Plot countplot for top 10 states
fig, ax = plt.subplots(figsize=(8,6))
sns.countplot(data=df_top_states, x="State", ax=ax,
              order=top_states)  # ensures sorted order
ax.set_title("Top 10 States by Incident Count")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
st.pyplot(fig)

# Add summary beneath chart
summary = (
    "This chart shows the distribution of incidents in the ten states with the highest counts. "
    f"The leading state is {top_states.iloc[0]}, followed by {top_states.iloc[1]} and {top_states.iloc[2]}. "
    "These states account for the majority of recorded incidents, highlighting regions most frequently affected."
)
st.write(summary)




##q7
st.subheader("7. Which states had the highest fatalities?")
state_deaths = df.groupby("State", as_index=False)["Number of deaths"].sum()
top_states = state_deaths.nlargest(5, "Number of deaths")
fig, ax = plt.subplots()
sns.barplot(data=top_states, x="State", y="Number of deaths", ax=ax)
ax.set_title("Top 5 States by Fatalities")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
st.pyplot(fig)
st.write(f"{top_states.iloc[0]['State']} recorded the highest fatalities overall, followed by {top_states.iloc[1]['State']} and {top_states.iloc[2]['State']}.")


##q8
st.subheader("8. Which years had the highest fatalities?")
year_deaths = df.groupby("Year", as_index=False)["Number of deaths"].sum()
top_years = year_deaths.nlargest(5, "Number of deaths")
fig, ax = plt.subplots()
sns.barplot(data=top_years, x="Year", y="Number of deaths", ax=ax)
ax.set_title("Top 5 Years by Fatalities")
st.pyplot(fig)
st.write(f"The year {top_years.iloc[0]['Year']} recorded the highest fatalities, followed by {top_years.iloc[1]['Year']} and {top_years.iloc[2]['Year']}.")


##q9
st.subheader("9. What is the distribution of fatalities across states?")

# Aggregate total deaths per state
state_deaths = df.groupby("State", as_index=False)["Number of deaths"].sum()

# Ensure numeric type
state_deaths["Number of deaths"] = pd.to_numeric(state_deaths["Number of deaths"], errors="coerce")

# Select top 10 states with highest fatalities
top_states = state_deaths.nlargest(10, "Number of deaths")["State"]

# Filter original dataframe to only those top 10 states
df_top_states = df[df["State"].isin(top_states)]

# Plot boxplot for top 10 states
fig, ax = plt.subplots(figsize=(8,6))
sns.boxplot(data=df_top_states, x="State", y="Number of deaths", ax=ax)
ax.set_title("Distribution of Fatalities in Top 10 States")
ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
st.pyplot(fig)

# Add summary beneath chart
summary = (
    "This boxplot shows the distribution of fatalities in the ten states with the highest overall death tolls. "
    f"The state with the largest total fatalities is {top_states.iloc[0]}, "
    f"followed by {top_states.iloc[1]} and {top_states.iloc[2]}. "
    "The spread and outliers highlight how some incidents in these states caused exceptionally high numbers of deaths."
)
st.write(summary)



###Identifier, Start date, End date, Number of deaths, State, Incident, 
# give 12 reserach question placing each into a subheader, and privde a seaborn,
#  matplotlib chart for each in streamlit app

