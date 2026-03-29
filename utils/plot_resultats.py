# Genere les graphes de l'exercice 4 du TP2

# lit les fichiers csv dans logs_exo4/ et genere 2 graphes :

#   1. graphe_comparaison.png : courbe moyenne du meilleur score au fil des evaluations pour RandomSearch2 et l'algorithme genetique (10 runs chacun) avec bande d'ecart-type pour voir la variabilite
#   2. graphe_un_run.png : exemple d'un seul run de chaque methode (meilleur score au fil du temps)


import os
import numpy as np
import matplotlib.pyplot as plt


def lire_csv(fichier):
    "lit le csv et retourne (evals, scores_courants, meilleurs_scores)"

    evals = []
    scores = []
    meilleurs = []

    with open(fichier, "r") as f:

        for line in f:
            line = line.strip()

            if not line:
                continue

            parts = line.split(",")
            evals.append(int(parts[0].strip()))
            scores.append(float(parts[1].strip()))
            meilleurs.append(float(parts[2].strip()))

    return evals, scores, meilleurs


def charger_tous_les_runs(prefixe):
    "charge tous les fichiers logs_exo4/{prefixe}_1.csv, _2.csv, etc"

    runs = []
    i = 1
    
    while True:
        fichier = "logs_exo4/" + prefixe + "_" + str(i) + ".csv"
        if not os.path.exists(fichier):
            break
    
        evals, scores, meilleurs = lire_csv(fichier)
        runs.append(meilleurs)
        i += 1
    
    return runs


def moyenne_et_ecart_type(runs):
    "calcule la moyenne et l'ecart-type sur les runs (alignes sur le plus court)"

    min_len = min(len(r) for r in runs)
    runs_alignes = [r[:min_len] for r in runs]
    data = np.array(runs_alignes)
    moyenne = np.mean(data, axis=0)
    ecart = np.std(data, axis=0)

    return moyenne, ecart, min_len


# Charger les donnees 

runs_rs2 = charger_tous_les_runs("log_randomsearch2")
runs_ga = charger_tous_les_runs("log_genetic")

# Graphe 1 : Comparaison moyenne sur 10 runs 

os.makedirs("logs_exo4", exist_ok=True)

plt.figure(figsize=(10, 6))

if len(runs_rs2) > 0:
    moy_rs2, std_rs2, n_rs2 = moyenne_et_ecart_type(runs_rs2)
    x_rs2 = range(1, n_rs2 + 1)
    plt.plot(x_rs2, moy_rs2, label="RandomSearch2 (moyenne)", color="blue")
    plt.fill_between(x_rs2, moy_rs2 - std_rs2, moy_rs2 + std_rs2, alpha=0.2, color="blue")

if len(runs_ga) > 0:
    moy_ga, std_ga, n_ga = moyenne_et_ecart_type(runs_ga)
    x_ga = range(1, n_ga + 1)
    plt.plot(x_ga, moy_ga, label="Algo genetique (moyenne)", color="red")
    plt.fill_between(x_ga, moy_ga - std_ga, moy_ga + std_ga, alpha=0.2, color="red")

plt.xlabel("Numero d'evaluation")
plt.ylabel("Meilleur score")
plt.title("Comparaison RandomSearch2 vs Algorithme Genetique\n(moyenne sur " + str(max(len(runs_rs2), len(runs_ga))) + " runs)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("logs_exo4/graphe_comparaison.png", dpi=150)

# Graphe 2 : Un seul run de chaque methode 

plt.figure(figsize=(10, 6))

if len(runs_rs2) > 0:
    plt.plot(range(1, len(runs_rs2[0]) + 1), runs_rs2[0], label="RandomSearch2 (run 1)", color="blue")

if len(runs_ga) > 0:
    plt.plot(range(1, len(runs_ga[0]) + 1), runs_ga[0], label="Algo genetique (run 1)", color="red")

plt.xlabel("Numero d'evaluation")
plt.ylabel("Meilleur score")
plt.title("Exemple d'un run unique")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("logs_exo4/graphe_un_run.png", dpi=150)

