import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Génération du jeu de données
np.random.seed(42)
n = 500
data = pd.DataFrame({
    'distance_km': np.random.randint(5, 300, size=n),
    'heure_envoi': np.random.randint(0, 24, size=n),
    'poids_kg': np.random.randint(1, 50, size=n),
    'jour_semaine': np.random.randint(0, 6, size=n),
    'zone_type': np.random.randint(0, 3, size=n),
})
data['retard'] = (
    (data['distance_km'] > 150).astype(int) +
    (data['zone_type'] == 2).astype(int) +
    (data['heure_envoi'] >= 15).astype(int)
)
data['retard'] = (data['retard'] > 1).astype(int)

# Séparation et entraînement
X = data.drop(columns=['retard'])
y = data['retard']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Sauvegarde
with open("modele_retard.pkl", "wb") as f:
    pickle.dump(model, f)

# Sauvegarde du dataset pour l'app
data.to_csv("livraisons.csv", index=False)
