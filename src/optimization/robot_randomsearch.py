import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from robot import *
import math

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch"
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

        # Phase de recherche aleatoire

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

                    # afficher le resultat
                    print("\tparams =", self.param, " score =", round(self.score_courant, 2))

                    # sauvegarder si meilleur
                    if self.score_courant > self.meilleur_score:
                        self.meilleur_score = self.score_courant
                        self.meilleur_param = list(self.param)
                        self.meilleur_eval = self.trial
                        print("\t*** nouveau meilleur score =", round(self.meilleur_score, 2), "a l'eval", self.meilleur_eval, "***")
                    
                    # verifier si le budget de strat est epuise (500 strategies)
                    if self.trial >= self.nb_evaluations:

                        print("\n========================================")
                        print("Recherche terminee\n")
                        print("Meilleur score  :", round(self.meilleur_score, 2))
                        print("Meilleurs params:", self.meilleur_param)
                        print("Trouve a l'eval :", self.meilleur_eval)
                        print("========================================")
                        self.phase_replay = True
                        self.compteur_replay = 0
                        self.iteration = self.iteration + 1
                        return 0, 0, True

                # nouveaux parametres aleatoires
                self.param = [random.randint(-1, 1) for i in range(8)]
                self.trial = self.trial + 1
                self.score_courant = 0
                self.translation_prec = 0
                self.rotation_prec = 0
                print("Trying strategy no.", self.trial)
                self.iteration = self.iteration + 1
                return 0, 0, True # ask for reset

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
