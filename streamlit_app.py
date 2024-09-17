import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API Keys
TOMORROW_API_KEY = "6k50priNXehOmPzaDaHK1IUvZd4bN9qj"
OS_API_KEY = "cxdWLKKk4uX7NoIzaAQyXDHtrJ0nhdgZ"  # Replace with your actual OS Names API key

# List of Swansea postcodes
swansea_postcodes = [
    'SA1', 'SA2', 'SA3', 'SA4', 'SA5', 'SA6', 'SA7', 'SA8', 'SA9',
    'SA18', 'SA19', 'SA20', 'SA31', 'SA32', 'SA33', 'SA34', 'SA35', 'SA36',
    'SA37', 'SA38', 'SA39', 'SA40', 'SA41', 'SA42', 'SA43', 'SA44', 'SA45',
    'SA46', 'SA47', 'SA48', 'SA61', 'SA62', 'SA63', 'SA64', 'SA65', 'SA66',
    'SA67', 'SA68', 'SA69', 'SA70', 'SA71', 'SA72', 'SA73'
]

def standardize_postcode(postcode):
    postcode = postcode.strip().replace(" ", "").upper()
    if len(postcode) > 3:
        return postcode[:-3] + " " + postcode[-3:]
    else:
        return postcode

def get_geocoding_data(postcode):
    # Remove spaces and convert to uppercase
    formatted_postcode = postcode.replace(" ", "").upper()
    
    url = f"https://api.os.uk/search/names/v1/find?query={formatted_postcode}&key={OS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            for result in data['results']:
                if result['GAZETTEER_ENTRY']['LOCAL_TYPE'] == 'Postcode':
                    lat = result['GAZETTEER_ENTRY']['GEOMETRY_Y']
                    lon = result['GAZETTEER_ENTRY']['GEOMETRY_X']
                    place_name = result['GAZETTEER_ENTRY'].get('POPULATED_PLACE', 'Unknown')
                    return lat, lon, place_name
            
            st.error(f"Postcode {postcode} not found in the results.")
            return None, None, None
        else:
            st.error(f"No results found for the postcode {postcode}.")
            return None, None, None
    else:
        st.error(f"Failed to retrieve geocoding data. Status code: {response.status_code}")
        st.error(f"API response: {response.text}")
        return None, None, None

def get_air_quality_data(lat, lon):
    url = "https://api.tomorrow.io/v4/timelines"
    params = {
        "location": f"{lat},{lon}",
        "fields": ["temperature", "humidity", "particulateMatter25", "particulateMatter10", "pollutantO3", "pollutantNO2", "pollutantCO"],
        "units": "metric",
        "timesteps": ["1h"],
        "timezone": "Europe/London",
        "apikey": TOMORROW_API_KEY
    }
    response = requests.post(url, json=params)
    if response.status_code == 200:
        data = response.json()
        return data['data']['timelines'][0]['intervals'][0]['values']
    else:
        st.error(f"Failed to retrieve air quality data. Status code: {response.status_code}")
        st.error(f"API response: {response.text}")
        return None

def get_alert_level(pm2_5):
    if pm2_5 is None:
        return "No Data", "gray", "Data not available."
    elif pm2_5 <= 5:
        return "No Alert", "green", "Particle pollution on your street is well below guideline levels. Air quality is not currently unhealthy, although woodburner use may increase levels in your area."
    elif 5 < pm2_5 <= 15:
        return "Advisory", "yellow", "Moderate particle pollution detected. Consider limiting woodburner use to reduce potential health impacts."
    else:
        return "Burner Alert", "red", "High particle pollution detected. Avoid using woodburners to prevent adverse health effects."

# Custom CSS
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
        background-color: #f8f4e3;
        border: 2px solid #dcd2a8;
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
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    postcode = st.text_input(':red[Enter your postcode] to determine if it is safe to use your wood stove')
    submit_postcode = st.button('Submit')
    
    if submit_postcode and postcode:
        standardized_postcode = standardize_postcode(postcode)
        
        if any(standardized_postcode.startswith(swansea_code) for swansea_code in swansea_postcodes):
            try:
                st.info(f"Attempting to geocode postcode: {standardized_postcode}")
                lat, lon, place_name = get_geocoding_data(standardized_postcode)
                if lat is not None and lon is not None:
                    st.success(f"Geocoding successful. Location: {place_name}")
                    air_quality_data = get_air_quality_data(lat, lon)
                    if air_quality_data:
                        pm2_5 = air_quality_data['particulateMatter25']
                        alert, color, alert_text = get_alert_level(pm2_5)
                        
                        st.markdown(f"<h2 class='sub-title'>Current Burner Alert Guideline for: {place_name} </h2>", unsafe_allow_html=True)
                        result_class = "result-gray" if color == "gray" else f"result-{color}"
                        st.markdown(f"<div class='result-box {result_class}'>"
                                    f"<div class='alert-status'>{alert}</div>"
                                    f"<div class='alert-text'>{alert_text}</div>"
                                    f"</div>", unsafe_allow_html=True)
                        
                        st.markdown(f"<h3 class='sub-title'>PM2.5 Level: {pm2_5} µg/m³</h3>", unsafe_allow_html=True)
                        
                        st.markdown(f"<div style='display: flex; justify-content: space-around;'>"
                                    f"<div style='background-color:green; padding: 10px; border-radius: 5px; color:white;'>0-5</div>"
                                    f"<div style='background-color:yellow; padding: 10px; border-radius: 5px; color:black;'>5-15</div>"
                                    f"<div style='background-color:red; padding: 10px; border-radius: 5px; color:white;'>>15</div>"
                                    f"</div>", unsafe_allow_html=True)
                    else:
                        st.error("Failed to retrieve air quality data.")
                else:
                    st.error("Could not get geolocation data for the provided postcode.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.error("Please check the postcode and try again.")
        else:
            st.error("The provided postcode is not within Swansea. Please enter a valid Swansea postcode.")
    else:
        st.markdown("<div class='info-box'>Burner Alert helps you determine if it is safe to use your wood stove based on the current PM2.5 air pollution levels in Swansea. Simply enter your postcode above to get started.</div>", unsafe_allow_html=True)

elif page == "Subscribe to Alerts":
    st.markdown("<h1 class='main-title'>Subscribe to Burner Alerts</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-title'>Subscribe to receive burner alerts via email</h2>", unsafe_allow_html=True)

    name = st.text_input('Enter your name:')
    email = st.text_input('Enter your email:') 
    sub_postcode = st.text_input('Enter the postcode you want alerts for:')

    if st.button('Subscribe'):
        if name and email and sub_postcode:
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
