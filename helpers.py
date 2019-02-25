import os

import pygame
import json
from consts import (
    BLUE,
    GREY,
    GameStatuses,
    SCREEN_SIZE
)


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


def get_abs_from_pygame_coords(coords: (int, int)):
    return (coords[0], SCREEN_SIZE[1] - coords[1])


def find_k(x, y):
    return y / x


def up_button_clicked(events) -> bool:
    return any([event.key in (pygame.K_UP, pygame.K_w)
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
