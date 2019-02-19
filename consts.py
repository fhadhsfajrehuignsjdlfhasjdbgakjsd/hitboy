SCREEN_SIZE = (1000, 550)  # pygame display size
BLUE = (173, 216, 230)
BLACK = (0, 0, 0)
HITBOY_SIZE = (35, 60)
HITBOY_START_POSITION = (100, 441)
FLOOR_RECT_POSITION = (0, 500, 1000, 50)  # x, y, width, height
G = 550
CHANGE_IMAGE_PERIOD = 3  # chagne hitboy image every n microseconds
OBSTACLE_SIZE = (40, 40)
OBSTACLE_START_POSITION = (960, 470)
OBSTACLE_IMAGES_NAMES = [
    'obstacle0.png'
]


class GameStatuses:
    MENU = 0
    PLAYING = 1
    PAUSE = 2
