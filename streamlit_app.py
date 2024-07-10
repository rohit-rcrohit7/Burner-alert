import streamlit as st 
import requests

# Hardcoded API key (replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key)
API_KEY = 'f598d541095a0ef824f1734f32b6f985'

# Function to get air pollution data from OpenWeatherMap
def get_air_pollution_data(lat, lon, api_key=API_KEY):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    pm2_5 = data['list'][0]['components']['pm2_5']
    return pm2_5

# Function to get geocoding data to convert postcode to latitude and longitude
def get_geocoding_data(postcode, api_key=API_KEY):
    url = f"http://api.openweathermap.org/geo/1.0/zip?zip={postcode},GB&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['lat'], data['lon']

# Function to determine the alert level
def get_alert_level(pm2_5):
    if pm2_5 <= 5:
        return "No Alert", "green"
    elif 5 < pm2_5 <= 15:
        return "Advisory", "yellow"
    else:
        return "Burner Alert", "red"

# Streamlit app title
st.markdown("<h1 style='text-align: center; color: white; background-color: red; border: 5px solid green; border-radius: 10px; padding: 10px;'>Burner Alert</h1>", unsafe_allow_html=True)

# Input for postcode
postcode = st.text_input('Enter your postcode:')

if postcode:
    try:
        lat, lon = get_geocoding_data(postcode)
        pm2_5 = get_air_pollution_data(lat, lon)
        alert, color = get_alert_level(pm2_5)

        # Display the results
        st.markdown(f"<h2 style='color: red;'>Current Burner Alert Guideline for: {postcode}</h2>")
        if color == "green":
            st.markdown(f"<p style='color:green; border: 2px solid green; border-radius: 5px; padding: 10px;'>Particle pollution on your street is well below guideline levels. Air quality is not currently unhealthy, although woodburner use may increase levels in your area.</p>", unsafe_allow_html=True)
        elif color == "yellow":
            st.markdown(f"<p style='color:orange; border: 2px solid orange; border-radius: 5px; padding: 10px;'>Particle pollution on your street is approaching guideline levels. Please consider not lighting your woodburner, particularly if you have an alternative source of heating.</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:red; border: 2px solid red; border-radius: 5px; padding: 10px;'>Particle pollution in this area is already above guideline levels. Avoid lighting your stove unless you do not have an alternative source of heating.</p>", unsafe_allow_html=True)

        # Display the PM2.5 value
        st.markdown(f"<h3 style='color: red;'>PM2.5 Level: {pm2_5} µg/m³</h3>")

        # Display the alert level
        st.markdown(f"<h2 style='text-align: center; color: {color}; border: 2px solid {color}; border-radius: 10px; padding: 10px;'>{alert}</h2>", unsafe_allow 
