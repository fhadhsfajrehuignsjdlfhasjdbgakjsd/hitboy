# general:
SCREEN_SIZE = (1000, 550)  # pygame display size
FLOOR_RECT_POSITION = (0, 500, 1000, 50)  # x, y, width, height
POINTER_SIZE = (20, 20)
ABOUT_URL = 'https://github.com/solemn-leader/hitboy/blob/master/README.md'
GAME_OVER_SOUND_NAME = 'audio/gameover.wav'
# colors:
BLUE = (173, 216, 230)
GREY = (211, 211, 211)
BLACK = (0, 0, 0)
# hitboy:
HITBOY_SIZE = (35, 60)
HITBOY_START_POSITION = (100, 441)
DEAD_HITBOY_SIZE = (60, 35)
DEAD_HITBOY_Y_POSITION = (465)
CHANGE_IMAGE_PERIOD = 3  # chagne hitboy image every n microseconds
# physics:
G = 2400
# obstacles
OBSTACLE_SIZE = (40, 40)
OBSTACLE_START_POSITION = (960, 470)
OBSTACLE_IMAGES_NAMES = [
    'obstacle0.png',
    'obstacle1.png',
    'obstacle2.png'
]
# menu
MENU_PLAY_ITEM_POSITION = (350, 100, 300, 100)
MENU_ABOUT_ITEM_POSITION = (350, 200, 300, 100)
MENU_RESTART_ITEM_POSITION = MENU_ABOUT_ITEM_POSITION
MENU_EXIT_ITEM_POSITION = (350, 300, 300, 100)
# score counter
SCORE_INITIAL_POSITION = (30, 50)
MAX_SCORE_INITIAL_POSITION = (30, 100)
# plane
PLANE_INITIAL_X_POSITION = 950
PLANE_Y_POSITION_RANGE = (50, 200)
PLANE_SIZE = (100, 50)
# weapon
WEAPON_INITIAL_POSITION = (95, 441)
WEAPON_SIZE = (60, 40)
# rocket
ROCKET_SIZE = (20, 10)


class GameStatuses:
    MENU = 0
    PLAYING = 1
    PAUSE = 2
    GAME_OVER = 3


class UserChoicesMenu:
    PLAY = 0
    ABOUT = 1
    EXIT = 2
    RESTART = 3
