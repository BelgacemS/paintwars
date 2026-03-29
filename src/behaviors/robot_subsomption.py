import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from robot import *

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Subsomption"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # Activation robot forte quand un robot est proche
        robot_stim = [1.0 - v for v in sensor_to_robot]

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        go_translation = sensors[sensor_front] * 1.0
        go_rotation = 0.0

        hatewall_translation = sensor_to_wall[sensor_front] * 1.0
        hatewall_rotation = (
            +1 * sensor_to_wall[sensor_front_left] +
            -1 * sensor_to_wall[sensor_front_right] +
            +1 * sensor_to_wall[sensor_left] +
            -1 * sensor_to_wall[sensor_right] +
            +1 * (1.0 - sensor_to_wall[sensor_front])
        )

        lovebot_translation = (
            robot_stim[sensor_front] +
            robot_stim[sensor_front_left] +
            robot_stim[sensor_front_right] +
            robot_stim[sensor_left] +
            robot_stim[sensor_right]
        )
        lovebot_rotation = (
            +1 * robot_stim[sensor_front_left] +
            -1 * robot_stim[sensor_front_right] +
            +1 * robot_stim[sensor_left] +
            -1 * robot_stim[sensor_right] +
            +1 * robot_stim[sensor_rear_left] +
            -1 * robot_stim[sensor_rear_right]
        )

        # Subsumption prio : eviter les murs > aller vers robots > tout droit
        wall_seen = min(sensor_to_wall) < 1.0
        robot_seen = min(sensor_to_robot) < 1.0

        if wall_seen:
            translation, rotation = hatewall_translation, hatewall_rotation
            active_behavior = "hatewall"
        elif robot_seen:
            translation, rotation = lovebot_translation, lovebot_rotation
            active_behavior = "lovebot"
        else:
            translation, rotation = go_translation, go_rotation
            active_behavior = "tout droit"

        if debug == True:
            if self.iteration % 100 == 0:
                print ("\tactive behavior               =", active_behavior)

        self.iteration = self.iteration + 1        
        return translation, rotation, False
