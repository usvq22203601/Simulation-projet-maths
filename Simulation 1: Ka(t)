import numpy as np
import matplotlib.pyplot as plt

# Paramètres
a = 10       # Capital initial de la compagnie   (millions €)
r = 1.5      # Prime annuelle fixe des primes d'assurance   (millions €/an)
lambda_C = 0.5  # Taux des coûts (1/c = 0.5 ⇒ c = 2)
max_time = 15  # Période de simulation (ans)

# Simulation d'une trajectoire
#np.random.seed(42)  # Pour fixer les valeurs

# 1. Génération des temps de sinistres (processus de Poisson)
deltas = np.random.exponential(scale=1.0, size=100)  # Δi ~ Exp(1)
# génère 100 intervalles de temps entre sinistres (Δi) suivant une lois exponentielle de paramètre 1
# le paramètre "scale" est définie comme 1/lambda, donc quand on mis 1, cad expérance = 1
# cela signifie que la moyenne du temps entre deux sinistres sera de 1 an
# mais en pratique, les valeurs de "deltas" varients

Tn = np.cumsum(deltas)  # Tn = ΣΔi
Tn = Tn[Tn <= max_time]  # On tronque à 20 ans

# 2. Génération des coûts des sinistres
nb_sinistre = len(Tn)
C = np.random.exponential(scale=1/lambda_C, size=nb_sinistre)  # Ci ~ Exp(0.5)
# génère des coûts aléatoires pour chaque sinistre, suivant une loi exponentielle de moyenne 2, car lambdaC = 0.5

# 3. Calcul du capital K(t) au cours du temps
time_points = np.linspace(0, max_time, 1000) # 1000 points entre 0 et 20 ans
Ka= np.zeros_like(time_points)
Ka[0] = a  #capital initial
Ci = 0  #à suivre combien de sinistres ont déjà été traités dans la simulation
C_total = 0  #coût cumulé des sinistres

for i in range(1, len(time_points)): #commence à i=1 car à i=0, on a capital initial =a
    t = time_points[i]
    dt = t - time_points[i-1]
    # Vérifier les sinistres survenus dans l'intervalle [t-dt, t]
    while Ci < nb_sinistre and Tn[Ci] <= t: #vérifie qu'il reste des sinistres non traitéssi et le sinistre est survenu 
                                            #avant t, on ajoute son coût 
        C_total += C[Ci] #coût de ce sinistre
        Ci += 1 #on passe au sinistre suivant
    Ka[i] = a + r * t - C_total

# Affichage
plt.figure(figsize=(10, 5))
plt.plot(time_points, Ka, label="Capital $K_a(t)$", color="blue")
plt.scatter(Tn, [a + r * t - np.sum(C[:i+1]) 
           for i, t in enumerate(Tn)], color="red", label="Sinistres")
plt.axhline(0, color="black", linestyle="--", label="Seuil de ruine")
plt.xlabel("Temps (années)")
plt.ylabel("Capital (millions €)")
plt.title(f"Simulation du capital d'une compagnie d'assurance\nNombre de sinistres = {nb_sinistre}")
plt.legend()
plt.grid(True)
plt.show()

# Résumé des sinistres
print(f"Nombre de sinistres en {max_time} ans : {nb_sinistre}")
print(f"Coût total des sinistres : {C_total:.2f} millions €")
print(f"Capital final : {Ka[-1]:.2f} millions €")
