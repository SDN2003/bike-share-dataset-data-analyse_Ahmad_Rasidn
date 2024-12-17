import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# Membuat Helper functions
def create_monthly_users_df(df):
    monthly_users_df = df.resample('M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    monthly_users_df['month'] = monthly_users_df['dteday'].dt.strftime('%b %Y')
    return monthly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    weekday_users_df['weekday'] = pd.Categorical(
        weekday_users_df['weekday'], 
        categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        ordered=True
    )
    weekday_users_df.sort_values('weekday', inplace=True)
    return weekday_users_df

def create_hourly_users_df(df):
    hourly_users_df = df.groupby("hr").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    return hourly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    seasonly_users_df['season'] = pd.Categorical(
        seasonly_users_df['season'], 
        categories=['Spring', 'Summer', 'Fall', 'Winter'],
        ordered=True
    )
    return seasonly_users_df

def create_weathersit_users_df(df):
    weathersit_users_df = df.groupby("weathersit").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    weathersit_users_df['weathersit'] = pd.Categorical(
        weathersit_users_df['weathersit'], 
        categories=['Clear', 'Mist', 'Light Snow', 'Heavy Rain'],
        ordered=True
    )
    return weathersit_users_df

def create_temp_users_df(df):
    bins = [0, 10, 20, 30, 40] 
    labels = ['0-10°C', '10-20°C', '20-30°C', '30-40°C']
    df['temp_range'] = pd.cut(df['temp'], bins=bins, labels=labels, include_lowest=True)

    temp_users_df = df.groupby('temp_range').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()

    return temp_users_df


df = pd.read_csv("https://raw.githubusercontent.com/SDN2003/bike-share-dataset-data-analyse_Ahmad_Rasidn/refs/heads/main/dashboard/new_bikeshare_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

st.title('Bikeshare Dashboard 🚴‍♂️')

min_date = df['dteday'].min()
max_date = df['dteday'].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/SDN2003/bike-share-dataset-data-analyse_Ahmad_Rasidn/refs/heads/main/etc/Designer.jpeg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
main_df = df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]

monthly_users_df = create_monthly_users_df(main_df)
weekday_users_df = create_weekday_users_df(main_df)
hourly_users_df = create_hourly_users_df(main_df)
seasonly_users_df = create_seasonly_users_df(main_df)
weathersit_users_df = create_weathersit_users_df(main_df)
temp_users_df = create_temp_users_df(main_df)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data

st.header("Visualisasi Data")

# Per bulan
st.subheader("Pengguna Per Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
monthly_users_df.set_index('month')[['casual', 'registered', 'cnt']].plot(kind='bar', ax=ax)
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Per hari
st.subheader("Pengguna Per Hari (Weekday)")
fig, ax = plt.subplots(figsize=(10, 5))
weekday_users_df.set_index('weekday')[['casual', 'registered', 'cnt']].plot(kind='bar', ax=ax)
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Per jam
st.subheader("Pengguna Per Jam")
fig, ax = plt.subplots(figsize=(10, 5))
hourly_users_df.set_index('hr')[['casual', 'registered', 'cnt']].plot(ax=ax)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel("Jam")
st.pyplot(fig)

# Per musim
st.subheader("Pengguna Per Musim")
fig, ax = plt.subplots(figsize=(10, 5))
seasonly_users_df.set_index('season')[['casual', 'registered', 'cnt']].plot(kind='bar', ax=ax)
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Per cuaca
st.subheader("Pengguna Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(10, 5))
weathersit_users_df.set_index('weathersit')[['casual', 'registered', 'cnt']].plot(kind='bar', ax=ax)
ax.set_ylabel("Jumlah Pengguna")
st.pyplot(fig)

# Per temperatur
st.subheader("Pengguna Berdasarkan Temperatur")
fig, ax = plt.subplots(figsize=(10, 5))
temp_users_df.set_index('temp_range')[['casual', 'registered', 'cnt']].plot(kind='bar', ax=ax)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel("Rentang Temperatur")
st.pyplot(fig)

st.caption("Copyright © Dicoding 2023")