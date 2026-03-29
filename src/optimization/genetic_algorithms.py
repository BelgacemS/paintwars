import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from robot import *
import math
import os

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "GeneticAlgorithm"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = []
    it_per_evaluation = 400
    trial = 0

    nb_evaluations = 0
    meilleur_score = -float('inf')
    meilleur_param = []
    meilleur_eval = -1
    score_courant = 0
    translation_prec = 0
    rotation_prec = 0
    phase_replay = False
    compteur_replay = 0

    # var pour algo genetic
    parent_param = []
    score_parent = -float('inf')

    nb_essais_par_strategie = 3
    essai_courant = 0

    log_csv = []  # pour l'exercice 4 

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation
        self.nb_evaluations = evaluations
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()
        # orientation aleatoire a chaque reset
        self.theta = random.uniform(0, 360)

    def mutation(self, parent):
        "Mutation : copie le parent et change un seul param"

        enfant = list(parent)

        i = random.randint(0, 7)
        valeurs = [-1, 0, 1]
        valeurs.remove(enfant[i])

        enfant[i] = random.choice(valeurs)

        return enfant

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # Phase de replay 

        if self.phase_replay:
            
            self.compteur_replay += 1

            # toutes les 1000 iterations, on remets a zero
            if self.compteur_replay % 1000 == 0:
                self.compteur_replay = 0

                return 0, 0, True 

            # les meilleur params
            translation = math.tanh( self.meilleur_param[0] + self.meilleur_param[1] * sensors[sensor_front_left] + self.meilleur_param[2] * sensors[sensor_front] + self.meilleur_param[3] * sensors[sensor_front_right] )
            rotation = math.tanh( self.meilleur_param[4] + self.meilleur_param[5] * sensors[sensor_front_left] + self.meilleur_param[6] * sensors[sensor_front] + self.meilleur_param[7] * sensors[sensor_front_right] )
            
            return translation, rotation, False

        # Phase d'algorithme genetique

        # calcul du score : contribution du pas precedent
        # on utilise les translations/rotations effectives

        if self.iteration > 0:

            delta_translation = self.log_sum_of_translation - self.translation_prec
            delta_rotation = self.log_sum_of_rotation - self.rotation_prec

            self.score_courant += delta_translation * (1 - delta_rotation)
            self.translation_prec = self.log_sum_of_translation
            self.rotation_prec = self.log_sum_of_rotation

        # toutes les it_per_evaluation iterations : evaluer et recommencer
        if self.iteration % self.it_per_evaluation == 0:
            if self.iteration > 0:

                self.essai_courant += 1

                # si on n'a pas encore fait les 3 essais : on recommence avec les memes params
                if self.essai_courant < self.nb_essais_par_strategie:
                    print("\t  essai", self.essai_courant, "/", self.nb_essais_par_strategie, " score partiel =", round(self.score_courant, 2))
                    self.translation_prec = 0
                    self.rotation_prec = 0
                    self.iteration += 1
                    return 0, 0, True  # reset avec nouvelle orientation

                # les 3 essais sont termines : on evalue la strategie
                print("\tparams =", self.param, " score total =", round(self.score_courant, 2))

                # si c'est le tout premier individu il devient le parent
                # sinon l'enfant remplace le parent seulement s'il est meilleur ou egal
                
                if self.trial == 1:
                    self.parent_param = list(self.param)
                    self.score_parent = self.score_courant
                    
                    print("\t  premier parent (score =", round(self.score_parent, 2), ")")
                
                else:
                    if self.score_courant >= self.score_parent:
                        self.parent_param = list(self.param)
                        self.score_parent = self.score_courant
                        
                        print("\t  -> enfant adopte comme nouveau parent")
                    
                    else:
                        print("\t  -> parent conserve (score parent =", round(self.score_parent, 2), ")")

                # sauvegarder si meilleur global
                if self.score_courant > self.meilleur_score:
                    self.meilleur_score = self.score_courant
                    self.meilleur_param = list(self.param)
                    self.meilleur_eval = self.trial
                    print("\t nouveau meilleur score =", round(self.meilleur_score, 2), "a l'eval", self.meilleur_eval, "***")

                # log CSV (exercice 4) : eval, score_courant, meilleur_score
                self.log_csv.append(str(self.trial) + ", " + str(round(self.score_courant, 2)) + ", " + str(round(self.meilleur_score, 2)))
                
                # verifier si le budget est epuise
                if self.trial >= self.nb_evaluations:

                    print("\n========================================")
                    print("Recherche terminee\n")
                    print("Meilleur score  :", round(self.meilleur_score, 2))
                    print("Meilleurs params:", self.meilleur_param)
                    print("Trouve a l'eval :", self.meilleur_eval)
                    print("========================================")

                    # ecrire le fichier CSV 
                    os.makedirs("logs_exo4", exist_ok=True)
                    run = 1
                    while os.path.exists("logs_exo4/log_genetic_" + str(run) + ".csv"):
                        run += 1
                    filename = "logs_exo4/log_genetic_" + str(run) + ".csv"
                    with open(filename, "w") as f:
                        for line in self.log_csv:
                            f.write(line + "\n")
                    print("Log sauvegarde dans", filename)

                    self.phase_replay = True
                    self.compteur_replay = 0
                    self.iteration += 1
                    return 0, 0, True

            # generer le prochain individu :
            # trial == 0 : premier parent aleatoire
            # trial > 0  : enfant = mutation du parent
            if self.trial == 0:
                self.param = [random.randint(-1, 1) for i in range(8)]
            else:
                self.param = self.mutation(self.parent_param)

            self.trial += 1
            self.score_courant = 0
            self.essai_courant = 0
            self.translation_prec = 0
            self.rotation_prec = 0
            print("Trying strategy no.", self.trial)
            self.iteration += 1
            return 0, 0, True  # reset avec orientation aleatoire

        # fonction de contrôle 
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1        

        return translation, rotation, False
