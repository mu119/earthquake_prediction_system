import streamlit as st
st.set_page_config(page_title="Earthquake Risk Predictor", layout="wide")

import pandas as pd
import numpy as np
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import plotly.express as px
from PIL import Image

# --- Branding & Header ---
logo = Image.open("data/logo.png")
st.image(logo, width=80)
st.markdown("<h1 style='text-align: center;'>🌍 Earthquake & Tsunami Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Powered by Historical Seismic Data and AI</h4>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🗌️ Navigation")
    st.markdown("Use tabs above to switch between prediction & data analysis.")
    st.markdown("---")
    st.subheader("📘 About This App")
    st.markdown("""
    This app predicts the earthquake and tsunami risk of any location based on:
    - Past seismic activity
    - Distance from historical earthquake points
    - Magnitude, depth, and tsunami impact
    """)
    st.markdown("---")
    st.markdown("📂 [View Dataset Source](https://example.com)")
    st.markdown("👨‍💼 Developed by Mukesh Nahar")

# -------- Load Data --------
@st.cache_data(show_spinner=True)
def load_data():
    df = pd.read_csv("data/earthquake_data.csv")
    df['date'] = pd.to_datetime(df['date'], errors='coerce', utc=True)
    df = df.dropna(subset=['date'])
    df['year'] = df['date'].dt.year

    def get_zone(lat, lon):
        if lat > 0 and -170 <= lon <= -30:
            return 'North America'
        elif lat > 0 and 30 <= lon <= 180:
            return 'Asia'
        elif lat > 35 and -30 <= lon <= 60:
            return 'Europe'
        elif lat < 0 and -80 <= lon <= -30:
            return 'South America'
        elif lat < 0 and 110 <= lon <= 180:
            return 'Oceania'
        elif lat < 0 and 20 <= lon <= 55:
            return 'Africa'
        elif lat < -60:
            return 'Antarctica'
        else:
            return 'Other'

    df['zone'] = df.apply(lambda row: get_zone(row['latitude'], row['longitude']), axis=1)
    return df

df = load_data()

# -------- Earthquake Risk Calculation --------
def calculate_earthquake_risk(input_lat, input_lon, df, radius_km=200):
    lat_min = input_lat - 2
    lat_max = input_lat + 2
    lon_min = input_lon - 2
    lon_max = input_lon + 2
    nearby_df = df[(df['latitude'] >= lat_min) & (df['latitude'] <= lat_max) &
                   (df['longitude'] >= lon_min) & (df['longitude'] <= lon_max)]

    risk_points = []
    input_location = (input_lat, input_lon)

    for _, row in nearby_df.iterrows():
        quake_location = (row['latitude'], row['longitude'])
        distance = geodesic(input_location, quake_location).km

        if distance <= radius_km:
            distance_weight = 1 - (distance / radius_km)
            magnitude_weight = min(row['magnitudo'] / 10, 1)
            depth_weight = 1 - min(row['depth'] / 700, 1)
            tsunami_weight = 1.5 if row['tsunami'] == 1 else 1.0

            risk = distance_weight * magnitude_weight * tsunami_weight * depth_weight
            risk_points.append(risk)

    if len(risk_points) == 0:
        return 0.0
    else:
        final_risk = np.clip(np.mean(risk_points) * 100, 0, 100)
        return round(final_risk, 2)

# -------- Tsunami Risk Calculation --------
def calculate_tsunami_risk(input_lat, input_lon, df, radius_km=200):
    lat_min = input_lat - 2
    lat_max = input_lat + 2
    lon_min = input_lon - 2
    lon_max = input_lon + 2
    nearby_df = df[(df['latitude'] >= lat_min) & (df['latitude'] <= lat_max) &
                   (df['longitude'] >= lon_min) & (df['longitude'] <= lon_max)]

    risk_points = []
    input_location = (input_lat, input_lon)

    for _, row in nearby_df.iterrows():
        if row['tsunami'] != 1:
            continue

        quake_location = (row['latitude'], row['longitude'])
        distance = geodesic(input_location, quake_location).km

        if distance <= radius_km:
            distance_weight = 1 - (distance / radius_km)
            magnitude_weight = min(row['magnitudo'] / 10, 1)
            depth_weight = 1 - min(row['depth'] / 700, 1)

            risk = distance_weight * magnitude_weight * depth_weight
            risk_points.append(risk)

    if len(risk_points) == 0:
        return 0.0
    else:
        final_risk = np.clip(np.mean(risk_points) * 100, 0, 100)
        return round(final_risk, 2)

# -------- Get Coordinates from Place --------
def get_lat_lon_from_place(place, df):
    match = df[df['place'].str.contains(place, case=False, na=False)]
    if not match.empty:
        return match.iloc[0]['latitude'], match.iloc[0]['longitude']

    try:
        geolocator = Nominatim(user_agent="quake_app")
        location = geolocator.geocode(place)
        if location:
            return location.latitude, location.longitude
    except:
        pass

    return None, None

# -------- Risk Wrapper --------
def get_risk_for_place(place, df):
    lat, lon = get_lat_lon_from_place(place, df)
    if lat is None or lon is None:
        return 0.0, 0.0, None, None

    radius = 150
    eq_risk = calculate_earthquake_risk(lat, lon, df, radius_km=radius)
    ts_risk = calculate_tsunami_risk(lat, lon, df, radius_km=radius)
    return eq_risk, ts_risk, lat, lon

# -------- Streamlit UI --------
tab1, tab2 = st.tabs(["🌍 Earthquake & Tsunami Prediction", "📊 EDA & Visual Analysis"])

with tab1:
    st.header("🌍 Earthquake & 🌊 Tsunami Risk Predictor")
    place = st.text_input("Enter location (e.g. Delhi, Chennai, Tokyo):", help="You can enter city names, states, or countries.")

    if place:
        with st.spinner("Calculating earthquake & tsunami risk..."):
            eq_risk, ts_risk, lat, lon = get_risk_for_place(place, df)

        if lat is None:
            st.error(f"'{place}' se koi location identify nahi ho paya. Risk: 0%")
        elif eq_risk == 0.0 and ts_risk == 0.0:
            st.warning(f"'{place}' ke 150 km ke radius me koi earthquake ya tsunami data nahi mila. Risk: 0%")
        else:
            st.success(f"Location: {place} | Latitude: {lat:.2f}, Longitude: {lon:.2f}")
            col1, col2 = st.columns(2)
            col1.metric("🌍 Earthquake Risk (%)", f"{eq_risk} %")
            col2.metric("🌊 Tsunami Risk (%)", f"{ts_risk} %")

with tab2:
    st.header("📊 Earthquake Data Analysis")

    st.subheader("1. Top 10 States with Most Earthquakes")
    top_states = df['state'].value_counts().head(10)
    st.bar_chart(top_states)

    st.subheader("2. Earthquake Magnitude Distribution")
    st.bar_chart(df['magnitudo'].value_counts().sort_index())

    st.subheader("3. Zone-wise Earthquake Frequency")
    zone_freq = df['zone'].value_counts()
    st.bar_chart(zone_freq)

    st.subheader("4. Year-wise Earthquake Count")
    year_freq = df['year'].value_counts().sort_index()
    st.line_chart(year_freq)

    st.subheader("5. 🌐 Earthquake Scatter Map (30,000 Sample Points)")
    df['depth_abs'] = df['depth'].abs()
    sample_size = 30000 if len(df) > 30000 else len(df)

    fig = px.scatter_geo(
        df.sample(sample_size),
        lat='latitude',
        lon='longitude',
        color='magnitudo',
        size='depth_abs',
        hover_name='date',
        hover_data={'depth': True, 'magnitudo': True},
        title='🌍 Global Earthquake Map',
        projection='natural earth',
        opacity=0.5,
        size_max=40,
        color_continuous_scale='Turbo'
    )

    fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
    fig.update_geos(center=dict(lat=20, lon=80), projection_scale=5, showcountries=True, countrycolor="RebeccaPurple")

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🔍 View Raw Earthquake Data (first 100 rows)"):
        st.dataframe(df.head(100))

    st.download_button("⬇️ Download Raw Dataset", df.to_csv(index=False), file_name='earthquake_data.csv')

# --- Footer ---
st.markdown("""<hr style="margin-top: 2rem; margin-bottom: 0.5rem;">""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>© 2025 Earthquake Risk App | Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
