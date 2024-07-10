import streamlit as st 
import requests

# Hardcoded API key (replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key)
API_KEY = 'YOUR_API_KEY'

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
________________________________________
From: Rohit Chakraborty <Rohit.Chakraborty@ukhsa.gov.uk>
Sent: Wednesday, July 10, 2024 9:44:08 AM
To: Rohit Chakraborty <Rohit.Chakraborty@ukhsa.gov.uk>
Subject: 
 
import streamlit as st 
import requests

# Function to get air pollution data from OpenWeatherMap
def get_air_pollution_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    pm2_5 = data['list'][0]['components']['pm2_5']
    return pm2_5

# Function to get geocoding data to convert postcode to latitude and longitude
def get_geocoding_data(postcode, api_key):
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
api_key = st.text_input('Enter your OpenWeatherMap API key:', type='password')

if postcode and api_key:
    try:
        lat, lon = get_geocoding_data(postcode, api_key)
        pm2_5 = get_air_pollution_data(lat, lon, api_key)
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
        st.markdown(f"<h2 style='text-align: center; color: {color}; border: 2px solid {color}; border-radius: 10px; padding: 10px;'>{alert}</h2>", unsafe_allow_html=True)

        # Display color-coded alert levels
        st.markdown(f"<div style='display: flex; justify-content: space-around;'>"
                    f"<div style='background-color:green; padding: 10px; border-radius: 5px;'>0-5</div>"
                    f"<div style='background-color:yellow; padding: 10px; border-radius: 5px;'>5-15</div>"
                    f"<div style='background-color:red; padding: 10px; border-radius: 5px;'>>15</div>"
                    f"</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error("Failed to retrieve data. Please check the postcode and API key.")
        st.error(str(e))
else:
    st.markdown("<h3 style='text-align: center; color: black;'>Find the burner alert status in your area</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: black;'>Enter your postcode and OpenWeatherMap API key to get the current air quality status for your area.</p>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        .css-1aumxhk {
            background-color: red !important;
            color: white !important;
            border: 2px solid green !important;
            border-radius: 5px !important;
        }
        .css-1aumxhk:hover {
            background-color: darkred !important;
            border: 2px solid darkgreen !important;
        }
        </style>
        """, unsafe_allow_html=True)
