import numpy as np                     # Pour les calculs mathématiques
import matplotlib.pyplot as plt        # Pour dessiner les graphiques
from matplotlib.lines import Line2D    # Pour personnaliser les légendes
plt.style.use('seaborn')               # Style joli pour les graphiques

def simulate_insurance(a, r, lambda_C, max_time, n_simulations=1):
    """
    Simule l'évolution du capital d'une compagnie d'assurance
    Paramètres:
    - a: capital initial
    - r: prime annuelle
    - lambda_C: paramètre de la loi exponentielle des coûts (1/c)
    - max_time: durée de simulation
    - n_simulations: nombre de simulations
    Retourne:
    - temps: points temporels
    - capital: évolution moyenne du capital
    - proba_ruine: probabilité de ruine
    - n_claims: nombre moyen de sinistres
    """
    all_Ka = []      # Pour stocker tous les résultats
    ruined = 0       # Compteur de faillites
    total_claims = 0 # Compteur total d'accidents
    
    for _ in range(n_simulations):
        # Génération des sinistres
        deltas = np.random.exponential(scale=1.0, size=100)
        Tn = np.cumsum(deltas)
        Tn = Tn[Tn <= max_time]
        n_claims = len(Tn)
        total_claims += n_claims
        
        # Génération des coûts
        C = np.random.exponential(scale=1/lambda_C, size=n_claims)
        
        # Calcul du capital
        time_points = np.linspace(0, max_time, 1000)
        Ka = np.zeros_like(time_points) # Tableau de zéros
        Ka[0] = a
        Ci = 0
        C_total = 0
        
        for i in range(1, len(time_points)):
            t = time_points[i]
            dt = t - time_points[i-1]
            while Ci < n_claims and Tn[Ci] <= t:
                C_total += C[Ci]
                Ci += 1
            Ka[i] = a + r * t - C_total
        
        all_Ka.append(Ka)
        if np.min(Ka) < 0: #Si l'argent devient négatif à un moment, on compte une faillite.
            ruined += 1
    
    return (time_points, 
            np.mean(all_Ka, axis=0), 
            ruined/n_simulations, 
            total_claims/n_simulations)

# Paramètres de simulation
a = 10       # Capital initial
max_time = 20  # Durée de simulation
n_simulations = 1000  # Nombre de simulations pour les stats

# Cas 1: c > r (1/c = 0.5 ⇒ c=2, r=1.5)
# Cas 2: c = r (1/c = 0.5 ⇒ c=2, r=2)
# Cas 3: c < r (1/c = 0.5 ⇒ c=2, r=2.5)
cases = [
    {'lambda_C': 0.5, 'r': 1.5, 'label': 'c > r (c=2, r=1.5)', 'color': 'red'},
    {'lambda_C': 0.5, 'r': 2.0, 'label': 'c = r (c=2, r=2)', 'color': 'blue'},
    {'lambda_C': 0.5, 'r': 2.5, 'label': 'c < r (c=2, r=2.5)', 'color': 'green'}
]

# Simulation et visualisation
plt.figure(figsize=(14, 8))

# 1. Evolution temporelle moyenne
for case in cases:
    time, Ka_mean, _, _ = simulate_insurance(a, case['r'], case['lambda_C'], max_time, 50)
    plt.plot(time, Ka_mean, label=case['label'], color=case['color'], linewidth=2)

plt.axhline(0, color='black', linestyle='--', label='Seuil de ruine')
plt.xlabel('Temps (années)', fontsize=12)
plt.ylabel('Capital moyen (millions €)', fontsize=12)
plt.title('Evolution du capital moyen pour les trois cas', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.show()

# 2. Statistiques de ruine
results = []
for case in cases:
    _, _, proba_ruine, avg_claims = simulate_insurance(a, case['r'], case['lambda_C'], max_time, n_simulations)
    results.append({
        'cas': case['label'],
        'proba_ruine': proba_ruine,
        'sinistres_moyens': avg_claims
    })

# Affichage des résultats
print("\nRésultats des simulations (sur {} runs):".format(n_simulations))
for res in results:
    print(f"\nCas {res['cas']}:")
    print(f"- Probabilité de ruine: {res['proba_ruine']:.2%}")
    print(f"- Nombre moyen de sinistres: {res['sinistres_moyens']:.1f}")

