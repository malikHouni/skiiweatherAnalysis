import streamlit as st
import requests
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Configuration de la page
st.set_page_config(page_title="Conditions Météorologiques de Ski", layout="wide")

# Titre de l'application
st.title("🌨️ Analyse des Conditions Météorologiques pour les Stations de Ski 🎿")

# Liste des stations de ski populaires
stations = [
    "Chamonix", "Courchevel", "Val d'Isère", "Les Arcs", "Zermatt", 
    "St. Anton", "Aspen", "Whistler", "Banff", "Tignes"
]

# Ajouter une clé API de OpenWeatherMap (remplacez par votre propre clé)
API_KEY = "149dc3c1376cc13a4c5d1a788e3be683"

# Demander à l'utilisateur de choisir une station dans la liste déroulante
station = st.selectbox("Choisissez une station de ski :", stations)

# Fonction pour récupérer les données météo
def get_weather_data(station):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={station}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Récupérer les données météo pour la station sélectionnée
weather_data = get_weather_data(station)

if weather_data:
    # Extraire les informations des données récupérées
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    weather_description = weather_data['weather'][0]['description']
    snow = weather_data['snow'] if 'snow' in weather_data else {'1h': 0}

    # Affichage des informations avec un peu de style
    st.subheader(f"🌤️ Conditions actuelles à {station.capitalize()} :")
    st.markdown(f"**Température** : {temp} °C")
    st.markdown(f"**Humidité** : {humidity} %")
    st.markdown(f"**Vitesse du vent** : {wind_speed} km/h")
    st.markdown(f"**Conditions météo** : {weather_description.capitalize()}")
    st.markdown(f"**Chutes de neige** : {snow.get('1h', 0)} cm dans l'heure")

    # Graphique des conditions météorologiques
    st.subheader("📊 Graphique des Conditions Météorologiques")
    labels = ['Température (°C)', 'Humidité (%)', 'Vitesse du Vent (km/h)', 'Neige (cm)']
    values = [temp, humidity, wind_speed, snow.get('1h', 0)]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(labels, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])

    # Ajouter des titres et labels aux axes
    ax.set_ylabel('Valeurs', fontsize=12)
    ax.set_title(f"Conditions Météorologiques à {station.capitalize()}", fontsize=14)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Y axis without decimals

    # Ajouter les valeurs sur chaque barre
    for i, v in enumerate(values):
        ax.text(i, v + 0.5, str(v), color='black', ha='center', fontsize=12)

    # Afficher le graphique
    st.pyplot(fig)

else:
    st.error(f"🚫 Impossible de récupérer les données météo pour {station}. Vérifie le nom de la station.")
