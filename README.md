# Paint Wars

Projet de L3 Informatique, UE IA & Jeux

Le but : programmer une équipe de 4 robots autonomes qui doivent conquérir le plus de cases possible dans une arène, face à une équipe adverse. Les robots n'ont que leurs capteurs (distance aux obstacles, type, équipe) et **un seul entier** en mémoire. Pas de communication entre eux, pas de carte.

## Demo

| Arena 0 (ouverte) | Arena 2 (couloirs) | Arena 4 (labyrinthe) |
|---|---|---|
| ![arena0](assets/arena_0.gif) | ![arena2](assets/arena_2.gif) | ![arena4](assets/arena_4.gif) |

Rouge = équipe OMEGA, Bleu = adversaire. Les cases colorées montrent le territoire conquis.

## Approche

### Comportements Braitenberg

5 comportements réactifs où la rotation et la translation dépendent directement des capteurs, sans if/else :
- Évitement d'obstacles, attraction/répulsion des murs, attraction/répulsion des robots

### Architecture de subsomption

Combinaison de comportements avec priorités : éviter les murs > aller vers les robots > avancer tout droit.

### Algorithme génétique

Optimisation des poids d'un perceptron (8 params) avec un (1+1)-ES :
- Mutation d'un seul param par génération
- Sélection : l'enfant remplace le parent que s'il est meilleur ou égal
- Chaque stratégie est évaluée 3 fois pour éviter le bruit
- J'ai aussi implémenté une recherche aléatoire pour comparer

### Stratégie finale (équipe OMEGA)

4 robots avec des rôles différents :

| Robot | Role | Description |
|-------|------|-------------|
| 0 | Explorateur | Braitenberg avec un peu d'aléatoire pour bien couvrir |
| 1 | Chasseur de couloirs | Détecte les couloirs et fonce tout droit dedans |
| 2 | Infiltrateur | Navigation asymétrique avec oscillation sinusoïdale |
| 3 | Sweeper | Hand-tuned + perceptron optimisé par l'algo génétique |

Tous les robots partagent :
- Du **bit-packing** pour stocker 5 infos dans un seul entier (position précédente, état, compteur de blocage, pas)
- Une **détection de blocage** : si le robot bouge plus pendant 10 pas, il tourne pour se débloquer
- Une **répulsion entre alliés** pour pas explorer les mêmes zones
- Une **poursuite des adversaires** quand ils sont détectés

## Structure du projet

```
├── src/
│   ├── tetracomposibot.py           # moteur de simulation (fourni)
│   ├── robot.py                      # classe de base Robot (fourni)
│   ├── robot_challenger.py           # stratégie finale
│   ├── robot_champion.py             # adversaire de référence (fourni)
│   ├── arenas.py / arenas_eval.py    # arènes de jeu
│   ├── config*.py                    # fichiers de configuration
│   ├── behaviors/                    # comportements réactifs
│   │   ├── robot_braitenberg_*.py    # 5 comportements Braitenberg
│   │   └── robot_subsomption.py      # architecture de subsomption
│   └── optimization/                 # algorithmes d'optimisation
│       ├── genetic_algorithms.py     # algo génétique (1+1)-ES
│       ├── robot_randomsearch.py     # recherche aléatoire
│       └── robot_randomsearch2.py    # recherche aléatoire améliorée
├── scripts/
│   ├── go_tournament                 # tournoi sur 5 arènes
│   └── go_tournament_eval            # tournoi complet sur 10 arènes
├── utils/
│   ├── plot_resultats.py             # visualisation des résultats
│   └── record_gif.py                 # enregistrement de GIFs
└── assets/                           # GIFs de demo
```

## Lancer le projet

```bash
pip install -r requirements.txt

# Un match
cd src
python tetracomposibot.py config_Paintwars

# Avec paramètres : arène (0-4), position (True/False), vitesse (0=normal, 1=rapide, 2=sans affichage)
python tetracomposibot.py config_Paintwars 1 False 1

# Tournoi complet (depuis la racine du projet)
sh scripts/go_tournament
```
