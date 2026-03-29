# Configuration par defaut

import arenas

display_mode = 0
arena = 0
position = False
max_iterations = 501

display_welcome_message = True
verbose_minimal_progress = True
display_robot_stats = True
display_team_stats = True
display_tournament_results = True
display_time_stats = True

import robot_challenger
import robot_champion

def initialize_robots(arena_size=-1, particle_box=-1):
    x_center = arena_size // 2
    y_center = arena_size // 2
    robots = []
    for i in range(4):
        robots.append(robot_challenger.Robot_player(4, y_center-16+i*8, 0, name="", team="A"))
    for i in range(4):
        robots.append(robot_champion.Robot_player(93, y_center-16+i*8, 180, name="", team="B"))
    return robots
