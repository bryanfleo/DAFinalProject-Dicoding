import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style = 'dark')

# Helper functions:

def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by = 'workingday').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean',})
    byworkingday_df = byworkingday_df.reset_index(drop = False)
    byworkingday_df['workingday'] = byworkingday_df['workingday'].replace([0, 1], ['Non-working day', 'Working day'])
    byworkingday_df = byworkingday_df.melt('workingday', var_name = 'Type', value_name = 'Count')
    
    return byworkingday_df


def create_byseason_df(df):
    byseason_df = df.groupby(by = ['season', 'hr']).agg({
        'cnt': 'mean'
    })
    byseason_df = byseason_df.reset_index(drop = False)
    
    return byseason_df


# Load data
df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")

df_day = df_day.drop(['instant', 'yr', 'mnth', 'holiday', 'weekday', 'atemp'], axis = 1)
df_hour = df_hour.drop(['instant', 'yr', 'mnth', 'holiday', 'weekday', 'atemp'], axis = 1)

df_day["dteday"] = pd.to_datetime(df_day["dteday"])
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])

# Filter data
min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label = 'Rentang Waktu',
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

# +
maindf_day = df_day[(df_day["dteday"] >= str(start_date)) & 
                (df_day["dteday"] <= str(end_date))]
maindf_hour = df_hour[(df_hour["dteday"] >= str(start_date)) & 
                (df_hour["dteday"] <= str(end_date))]

maindf_day = maindf_day.drop(['dteday'], axis = 1)
maindf_hour = maindf_hour.drop(['dteday'], axis = 1)
# -

# Menyiapkan berbagai dataframe
byworkingday_df = create_byworkingday_df(maindf_day)
byseason_df = create_byseason_df(maindf_hour)


# Plot daily rentals by working day
st.header('Bike Sharing Dashboard :bike:')
st.subheader('Average Daily Rentals')

col1, col2 = st.columns(2)

with col1:
    mean_workingday = byworkingday_df['Count'].iloc[[5]]
    st.metric("Working days", value = mean_workingday)

with col2:
    mean_nonworkingday = byworkingday_df['Count'].iloc[[4]]
    st.metric("Non-working days", value = mean_nonworkingday)

fig, ax = plt.subplots(figsize = (16, 12))
sns.barplot(data = byworkingday_df, x = 'Type', y = 'Count', hue = 'workingday', errorbar = None)

st.pyplot(fig)


# Plot of hourly bike rentals by season
st.subheader("Average Hourly Rentals by Season")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    ax.plot(
        byseason_df[byseason_df['season'] == 1]['hr'],
        byseason_df[byseason_df['season'] == 1]['cnt'],
        marker = 'o', 
        linewidth = 2,
        color = "#FF598F")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("Spring", loc = "center", fontsize = 30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    ax.plot(
        byseason_df[byseason_df['season'] == 2]['hr'],
        byseason_df[byseason_df['season'] == 2]['cnt'],
        marker = 'o', 
        linewidth = 2,
        color = "#F3BC2E")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("Summer", loc = "center", fontsize = 30)
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots(figsize=(20, 10))

    ax.plot(
        byseason_df[byseason_df['season'] == 3]['hr'],
        byseason_df[byseason_df['season'] == 3]['cnt'],
        marker = 'o', 
        linewidth = 2,
        color = "#D45B12")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("Autumn", loc = "center", fontsize = 30)
    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots(figsize=(20, 10))

    ax.plot(
        byseason_df[byseason_df['season'] == 4]['hr'],
        byseason_df[byseason_df['season'] == 4]['cnt'],
        marker = 'o', 
        linewidth = 2,
        color = "#42687C")
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.set_title("Winter", loc = "center", fontsize = 30)
    st.pyplot(fig)

st.caption('Bryan Florentino Leo - 2024')
