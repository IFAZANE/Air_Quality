import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Clé API WeatherAPI
API_KEY = "7297e29b406a403ab5873732252704"  # Remplace par ta clé API

st.title("🌍 Pollution de l'Air en Temps Réel")

# Saisie de la ville par l'utilisateur
ville = st.text_input("🏙️ Entrez une ville (ex: Lomé)", "Lome")

if st.button("🔄 Vérification de l'état de pollution de la ville! (Cliquer ici)"):

    # Appel à l'API WeatherAPI pour récupérer les données météo et AQI
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={ville}&aqi=yes"
    response = requests.get(url)

    if response.status_code != 200:
        st.error("Erreur lors de la récupération des données. Vérifiez la ville ou la clé API.")
    else:
        # Extraire les données de la réponse JSON
        data = response.json()
        current = data["current"]
        air = current.get("air_quality", {})

        # Affichage des données météo actuelles
        st.markdown("### 🌤️ Données météo actuelles")
        st.write(f"Température : {current['temp_c']} °C")
        st.write(f"Humidité : {current['humidity']} %")
        st.write(f"Pression : {current['pressure_mb']} mb")
        st.write(f"Vent : {current['wind_kph']} km/h")
        st.write(f"Indice UV : {current['uv']}")

        # Affichage des vraies valeurs de pollution en temps réel
        st.markdown("### 🧪 Valeurs réelles de pollution")
        pm25 = air.get('pm2_5', 'n/a')
        pm10 = air.get('pm10', 'n/a')
        no2 = air.get('no2', 'n/a')
        so2 = air.get('so2', 'n/a')
        o3 = air.get('o3', 'n/a')

        st.write(f"PM2.5 : {pm25}")
        st.write(f"PM10 : {pm10}")
        st.write(f"NO2 : {no2}")
        st.write(f"SO2 : {so2}")
        st.write(f"O3 : {o3}")

        # Affichage d'un graphique en barres avec les valeurs de pollution
        pollution_data = {
            'Polluant': ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3'],
            'Valeur': [pm25 if isinstance(pm25, (int, float)) else 0,
                       pm10 if isinstance(pm10, (int, float)) else 0,
                       no2 if isinstance(no2, (int, float)) else 0,
                       so2 if isinstance(so2, (int, float)) else 0,
                       o3 if isinstance(o3, (int, float)) else 0]
        }
        df_pollution = pd.DataFrame(pollution_data)

        # Création du graphique avec matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(df_pollution['Polluant'], df_pollution['Valeur'], color=['blue', 'orange', 'green', 'red', 'purple'])
        ax.set_title(f"Situation de la pollution de l'air à {ville}")
        ax.set_ylabel("Concentration (µg/m³)")
        ax.set_xlabel("Polluants")
        st.pyplot(fig)

        # Création d'un graphique interactif avec plotly
        fig_plotly = px.bar(df_pollution, x='Polluant', y='Valeur', color='Polluant',
                            title=f"Pollution de l'air à {ville}",
                            labels={'Valeur': 'Concentration (µg/m³)', 'Polluant': 'Type de polluant'})
        st.plotly_chart(fig_plotly)

        # Affichage de l'interprétation de la qualité de l'air
        st.markdown("### 🌬️ Interprétation de la qualité de l'air")
        if isinstance(pm25, (int, float)) and pm25 <= 10:
            st.info("Qualité de l'air : Bonne 👍")
        elif isinstance(pm25, (int, float)) and pm25 <= 25:
            st.info("Qualité de l'air : Modérée")
        elif isinstance(pm25, (int, float)) and pm25 <= 50:
            st.warning("Qualité de l'air : Mauvaise - Sensible pour les groupes à risque")
        else:
            st.error("Qualité de l'air : Très mauvaise ❌")

st.text("🏙️ Kpatchaa te remercie pour ta confiance")