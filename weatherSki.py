import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Clé API OpenWeatherMap
API_KEY = st.secrets["weather_API_KEY"]

# Hugging Face Inference API Settings
HF_TOKEN = st.secrets["mistral_API_KEY"]
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"  # Replace with the model you wish to use

# Liste des stations de ski avec coordonnées
stations_ski = {
    "Courchevel": (45.4154, 6.6345),
    "Val Thorens": (45.2979, 6.5790),
    "Chamonix": (45.9237, 6.8694),
    "Tignes": (45.4681, 6.9054),
    "Les Arcs": (45.5724, 6.8281),
    "Méribel": (45.3963, 6.5652),
    "Avoriaz": (46.1912, 6.7706),
}

# Interface Streamlit
st.title("🏔️ Météo & Chatbot des Stations de Ski")

station = st.selectbox("Choisissez une station :", list(stations_ski.keys()))

# API OpenWeatherMap
URL = "https://api.openweathermap.org/data/2.5/weather"
params = {"q": station, "appid": API_KEY, "units": "metric", "lang": "fr"}

response = requests.get(URL, params=params)

if response.status_code == 200:
    data = response.json()
    icon_code = data["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

    st.success(f"📍 **{station}** - {data['weather'][0]['description'].capitalize()}")
    st.image(icon_url, width=100)
    st.metric(label="🌡 Température", value=f"{data['main']['temp']}°C")
    st.metric(label="💨 Vent", value=f"{data['wind']['speed']} m/s")
    st.metric(label="💧 Humidité", value=f"{data['main']['humidity']}%")

    # Carte Folium
    st.subheader("📌 Localisation de la station")
    station_coords = stations_ski[station]
    map_ski = folium.Map(location=station_coords, zoom_start=10)
    folium.Marker(station_coords, popup=station, icon=folium.Icon(color="blue")).add_to(map_ski)
    folium_static(map_ski)

else:
    st.error(f"🚫 Impossible de récupérer la météo pour {station}. Vérifie l'API.")

# 💬 Chatbot Hugging Face
st.subheader("💬 Chatbot Ski & Météo")
user_input = st.text_input("Pose une question sur la météo ou la station :")

if user_input:
    # Contexte intelligent pour guider le modèle
    contexte = f"""
    Actuellement, la météo à {station} est :
    - Température : {data['main']['temp']}°C
    - Vent : {data['wind']['speed']} m/s
    - Humidité : {data['main']['humidity']}%
    - Conditions : {data['weather'][0]['description'].capitalize()}

    Question : {user_input}
    Réponse :
    """

    # API request to Hugging Face Inference
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": contexte,
        "options": {"use_cache": False},
    }

    api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    api_response = requests.post(api_url, headers=headers, json=payload)

    if api_response.status_code == 200:
        response_data = api_response.json()
        st.write("🤖 " + response_data[0]["generated_text"])
    else:
        st.error(f"🚫 Error in reaching the API: {api_response.status_code} - {api_response.text}")
