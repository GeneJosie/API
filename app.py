
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(layout="wide")
st.title("📦 Optimisation des Livraisons – Transatlantic SA")

# Chargement du modèle
with open("modele_retard.pkl", "rb") as f:
    model = pickle.load(f)

# Chargement des données
data = pd.read_csv("livraisons.csv")

# Interface utilisateur
st.sidebar.header("🛠️ Paramètres de livraison")
distance = st.sidebar.slider("Distance (km)", 1, 300, 50)
heure = st.sidebar.slider("Heure d’envoi", 0, 23, 14)
poids = st.sidebar.slider("Poids du colis (kg)", 1, 50, 10)
jour = st.sidebar.selectbox("Jour de la semaine", ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"])
zone = st.sidebar.selectbox("Type de zone", ["Urbaine", "Périurbaine", "Rurale"])

# Mapping pour l'encodage
jour_map = {"Lundi": 0, "Mardi": 1, "Mercredi": 2, "Jeudi": 3, "Vendredi": 4, "Samedi": 5}
zone_map = {"Urbaine": 0, "Périurbaine": 1, "Rurale": 2}

# Prédiction
features = [[distance, heure, poids, jour_map[jour], zone_map[zone]]]
prediction = model.predict(features)[0]
proba = model.predict_proba(features)[0][1]

# Affichage du résultat
st.subheader("🎯 Résultat de la prédiction")
if prediction == 1:
    st.error(f"⚠️ Risque élevé de retard ({proba:.0%})")
else:
    st.success(f"✅ Livraison attendue dans les délais ({(1 - proba):.0%})")

# Carte interactive
st.subheader("🗺️ Carte des livraisons simulées")
m = folium.Map(location=[4.05, 9.7], zoom_start=6)
marker_cluster = MarkerCluster().add_to(m)

for _, row in data.iterrows():
    lat = 4 + (np.random.rand() - 0.5) * 2  # Coordonnées aléatoires simulées
    lon = 10 + (np.random.rand() - 0.5) * 2
    couleur = "green" if row["retard"] == 0 else "red"
    folium.Marker(
        location=[lat, lon],
        popup=f"Distance: {row['distance_km']} km | Poids: {row['poids_kg']} kg",
        icon=folium.Icon(color=couleur)
    ).add_to(marker_cluster)

st_folium(m, width=1000, height=500)

# Statistiques globales
st.subheader("📊 Statistiques générales")
col1, col2 = st.columns(2)
col1.metric("Livraisons totales", len(data))
col2.metric("Livraisons à risque", int(data["retard"].sum()))
