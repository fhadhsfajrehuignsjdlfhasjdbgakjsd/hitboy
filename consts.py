# general:
SCREEN_SIZE = (1000, 550)  # pygame display size
FLOOR_RECT_POSITION = (0, 500, 1000, 50)  # x, y, width, height
ABOUT_URL = 'https://github.com/solemn-leader/hitboy/blob/master/README.md'
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
G = 1200
# obstacles
OBSTACLE_SIZE = (40, 40)
OBSTACLE_START_POSITION = (960, 470)
OBSTACLE_IMAGES_NAMES = [
    'obstacle0.png',
    'obstacle1.png'
]
# menu
MENU_PLAY_ITEM_POSITION = (350, 100, 300, 100)
MENU_ABOUT_ITEM_POSITION = (350, 200, 300, 100)
MENU_RESTART_ITEM_POSITION = MENU_ABOUT_ITEM_POSITION
MENU_EXIT_ITEM_POSITION = (350, 300, 300, 100)


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

