import os

import pygame
import json
from consts import (
    BLUE,
    GREY,
    GameStatuses,
    SCREEN_SIZE,
    GAME_OVER_SOUND_NAME
)
from math import sin
import numpy as np


def find_k_and_b(x1, y1, x2, y2):
    a = np.array([[x1, 1], [x2, 1]])
    b = np.array([y1, y2])
    try:
        k, b = np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        k, b = None, None
    return k, b


def load_image(name):
    '''gets image from images folder'''
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


def clean_screen(screen, game_status):
    if game_status == GameStatuses.PLAYING:
        screen.fill(BLUE)
    elif game_status == GameStatuses.MENU:
        screen.fill(GREY)


def check_exit(events) -> bool:
    return any([event.type == pygame.QUIT for event in events])


def check_pause(events) -> bool:
    return any([event.key == pygame.K_ESCAPE
                for event in events if event.type == pygame.KEYDOWN])
    

def where_to_shoot(events) -> (int, int):
    '''gets the point where user clicks in pygame system
    returns (-1, -1) if we must not shoot'''
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            return pos
    return (-1, -1)


def up_button_clicked(events) -> bool:
    return any([event.key in (pygame.K_UP, pygame.K_w, pygame.K_SPACE)
                for event in events if event.type == pygame.KEYDOWN])


def get_max_score() -> int:
    try:
        with open('hitboy.json', 'r') as file:
            data = json.load(file)
            return data['max_score']
    except FileNotFoundError:
        set_max_score(0)
        return 0


def set_max_score(n_score):
    with open('hitboy.json', 'w') as file:
        json.dump({'max_score': int(n_score)}, file)


def get_rocket_speed_by_angle(rotation_angle):
    x_speed = 0
    sign = 1
    if rotation_angle >= 90:
        rotation_angle = 180 - rotation_angle
        sign = -1
    if rotation_angle <= 55:
        x_speed = 600
    elif rotation_angle <= 70:
        x_speed = 350
    elif rotation_angle <= 75:
        x_speed = 250
    elif rotation_angle <= 85:
        x_speed = 125
    elif rotation_angle <= 88:
        x_speed = 65
    elif rotation_angle <= 89:
        x_speed = 20
    else:
        x_speed = 5
    return x_speed * sign


def get_angle_by_three_points(point1, point2, point3) -> int:
    a = np.array([*point1])
    b = np.array([*point2])
    c = np.array([*point3])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return int(np.degrees(angle))


def get_point_on_same_line(point1):
    return (point1[0] + 1, point1[1])


def finish_game(score) -> int:
    score.check_new_max_score()
    pygame.mouse.set_visible(True)
    pygame.mixer.Sound(GAME_OVER_SOUND_NAME).play()
    return GameStatuses.GAME_OVER
