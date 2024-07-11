import streamlit as st 
import requests
import os
import pandas as pd
from datetime import datetime

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
os.environ['API_KEY'] = st.secrets['API_KEY']
API_KEY = os.getenv('API_KEY')

# List of Swansea postcodes
swansea_postcodes = [
    'SA1', 'SA2', 'SA3', 'SA4', 'SA5', 'SA6', 'SA7', 'SA8', 'SA9',
    'SA18', 'SA19', 'SA20', 'SA31', 'SA32', 'SA33', 'SA34', 'SA35', 'SA36',
    'SA37', 'SA38', 'SA39', 'SA40', 'SA41', 'SA42', 'SA43', 'SA44', 'SA45',
    'SA46', 'SA47', 'SA48', 'SA61', 'SA62', 'SA63', 'SA64', 'SA65', 'SA66',
    'SA67', 'SA68', 'SA69', 'SA70', 'SA71', 'SA72', 'SA73'
]

# Function to standardize the postcode
def standardize_postcode(postcode):
    postcode = postcode.strip().replace(" ", "").upper()
    if len(postcode) > 3:
        return postcode[:-3] + " " + postcode[-3:]
    else:
        return postcode

# Function to get air pollution data from OpenWeatherMap
def get_air_pollution_data(lat, lon, api_key=API_KEY):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'list' in data and len(data['list']) > 0:
        pm2_5 = data['list'][0]['components']['pm2_5']
        return pm2_5
    else:
        st.error("Failed to retrieve air pollution data.")
        return None

# Function to get geocoding data to convert postcode to latitude, longitude, and place name
def get_geocoding_data(postcode, api_key=API_KEY):
    url = f"http://api.openweathermap.org/geo/1.0/zip?zip={postcode},GB&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'lat' in data and 'lon' in data and 'name' in data:
        return data['lat'], data['lon'], data['name']
    elif 'lat' in data and 'lon' in data:
        return data['lat'], data['lon'], postcode  # Fallback to postcode if place name is not available
    else:
        st.error("Failed to retrieve geocoding data. Please check the postcode.")
        return None, None, None

# Function to determine the alert level
def get_alert_level(pm2_5):
    if pm2_5 is None:
        return "No Data", "gray", "Data not available."
    elif pm2_5 <= 5:
        return "No Alert", "green", "Particle pollution on your street is well below guideline levels. Air quality is not currently unhealthy, although woodburner use may increase levels in your area."
    elif 5 < pm2_5 <= 15:
        return "Advisory", "yellow", "Moderate particle pollution detected. Consider limiting woodburner use to reduce potential health impacts."
    else:
        return "Burner Alert", "red", "High particle pollution detected. Avoid using woodburners to prevent adverse health effects."

# Custom CSS for Swansea-themed styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: white;
        background-color: red;
        border: 5px solid green;
        border-radius: 10px;
        padding: 10px;
    }
    .sub-title {
        color: darkred;
        text-align: center;
        margin-top: 20px;
    }
    .description {
        text-align: center;
        color: darkgreen;
    }
    .result-box {
        border: 2px solid;
        border-radius: 5px;
        padding: 10px;
        margin: 10px;
        text-align: center;
    }
    .result-green {
        border-color: green;
        color: green;
    }
    .result-yellow {
        border-color: orange;
        color: orange;
    }
    .result-red {
        border-color: red;
        color: red;
    }
    .result-gray {
        border-color: gray;
        color: gray;
    }
    .alert-status {
        font-weight: bold;
    }
    .alert-text {
        font-weight: normal;
    }
    .instructions {
        text-align: center;
        color: black;
        margin-top: 20px;
    }
    .info-box {
        background-color: #f8f4e3; /* Light beige */
        border: 2px solid #dcd2a8; /* Matching border color */
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-family: Arial, sans-serif;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Burner Alert Status", "Subscribe to Alerts"])

if page == "Burner Alert Status":
    st.markdown("<h1 class='main-title'>Burner Alert</h1>", unsafe_allow_html=True)
    st.subheader(':red[Enter your postcode] to determine if it is safe to use your wood stove')
   

    # Input for postcode
    postcode = st.text_input('Swansea Postcode')

    if postcode:
        # Standardize the postcode input
        standardized_postcode = standardize_postcode(postcode)
        
        if any(standardized_postcode.startswith(swansea_code) for swansea_code in swansea_postcodes):
            try:
                lat, lon, place_name = get_geocoding_data(standardized_postcode)
                if lat is not None and lon is not None:
                    pm2_5 = get_air_pollution_data(lat, lon)
                    alert, color, alert_text = get_alert_level(pm2_5)
                    
                    # Display the results
                    st.markdown(f"<h2 class='sub-title'>Current Burner Alert Guideline for: {place_name} ({standardized_postcode})</h2>", unsafe_allow_html=True)
                    result_class = "result-gray" if color == "gray" else f"result-{color}"
                    st.markdown(f"<div class='result-box {result_class}'>"
                                f"<div class='alert-status'>{alert}</div>"
                                f"<div class='alert-text'>{alert_text}</div>"
                                f"</div>", unsafe_allow_html=True)
                    
                    # Display the PM2.5 value
                    if pm2_5 is not None:
                        st.markdown(f"<h3 class='sub-title'>PM2.5 Level: {pm2_5} µg/m³</h3>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<h3 class='sub-title'>PM2.5 Level: Data not available</h3>", unsafe_allow_html=True)
                    
                    # Display color-coded alert levels
                    st.markdown(f"<div style='display: flex; justify-content: space-around;'>"
                                f"<div style='background-color:green; padding: 10px; border-radius: 5px; color:white;'>0-5</div>"
                                f"<div style='background-color:yellow; padding: 10px; border-radius: 5px; color:black;'>5-15</div>"
                                f"<div style='background-color:red; padding: 10px; border-radius: 5px; color:white;'>>15</div>"
                                f"</div>", unsafe_allow_html=True)
                else:
                    st.error("Could not get geolocation data for the provided postcode.")
            except Exception as e:
                st.error("Failed to retrieve data. Please check the postcode and API key.")
                st.error(str(e))
        else:
            st.error("The provided postcode is not within Swansea. Please enter a valid Swansea postcode.")
    else:
        st.markdown("<div class='info-box'>Burner Alert helps you determine if it is safe to use your wood stove based on the current PM2.5 air pollution levels in Swansea. Simply enter your postcode above to get started.</div>", unsafe_allow_html=True)

elif page == "Subscribe to Alerts":
    st.markdown("<h1 class='main-title'>Subscribe to Burner Alerts</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Subscribe to receive burner alerts via email</h2>", unsafe_allow_html=True)

    # Input for subscription
    name = st.text_input('Enter your name:')
    email = st.text_input('Enter your email:') 
    sub_postcode = st.text_input('Enter the postcode you want alerts for:')

    if st.button('Subscribe'):
        if name and email and sub_postcode:
            # Standardize the postcode input
            standardized_sub_postcode = standardize_postcode(sub_postcode)
            if any(standardized_sub_postcode.startswith(swansea_code) for swansea_code in swansea_postcodes):
                subscription = {'name': name, 'email': email, 'postcode': standardized_sub_postcode, 'subscribed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                subscriptions = pd.DataFrame([subscription])
                subscriptions.to_csv('subscriptions.csv', mode='a', header=False, index=False)
                st.success('You have successfully subscribed to Burner Alerts!')
            else:
                st.error('The provided postcode is not within Swansea. Please enter a valid Swansea postcode.')
        else:
            st.error('Please enter your name, email, and the postcode you want alerts for.')

