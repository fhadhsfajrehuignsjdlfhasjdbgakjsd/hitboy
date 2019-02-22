import os

import pygame
from consts import BLUE


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
    screen.fill(BLUE)


def check_exit(events) -> bool:
    return any([event.type == pygame.QUIT for event in events])


def up_button_clicked(events) -> bool:
    return any([event.key in (pygame.K_UP, pygame.K_w)
                for event in events if event.type == pygame.KEYDOWN])


def display_menu(screen):
    pass
