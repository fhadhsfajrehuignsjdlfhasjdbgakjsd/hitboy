import pygame
import webbrowser
from consts import *
import threading

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

from helpers import *
from entities import (
    entities, 
    obstacles, 
    menu, 
    pause_menu,
    start_new_game,
    add_obstacle_if_necessary
)

timer = pygame.time.Clock()
# pygame.mixer.init()
# pygame.mixer.music.load("audio/monster.mp3")
# pygame.mixer.music.play()
game_status = GameStatuses.MENU
pygame.display.set_caption('Hitboy.')
pygame.display.set_icon(load_image('favicon.png'))

while True:
    time_passed_in_secs = timer.tick(60) / 1000
    if game_status == GameStatuses.GAME_OVER:
        menu.draw(screen)
        events = pygame.event.get()
        if check_exit(events):
            pygame.quit()
            exit(0)
        user_choice = menu.get_user_choice(events)
        if user_choice is not None:
            if user_choice == UserChoicesMenu.PLAY:
                game_status = GameStatuses.PLAYING
                entities, obstacles = start_new_game(entities, obstacles)                
            elif user_choice == UserChoicesMenu.EXIT:
                pygame.quit()
                exit(0)
            elif user_choice == UserChoicesMenu.ABOUT:
                webbrowser.open(ABOUT_URL)

    elif game_status == GameStatuses.PAUSE:
        pause_menu.draw(screen)
        events = pygame.event.get()
        if check_exit(events):
            pygame.quit()
            exit(0)
        user_choice = pause_menu.get_user_choice(events)
        if user_choice is not None:
            if user_choice == UserChoicesMenu.PLAY:
                game_status = GameStatuses.PLAYING
            elif user_choice == UserChoicesMenu.EXIT:
                pygame.quit()
                exit(0)
            elif user_choice == UserChoicesMenu.RESTART:
                game_status = GameStatuses.PLAYING
                entities, obstacles = start_new_game(entities, obstacles)
            if user_choice == UserChoicesMenu.PLAY:
                    game_status = GameStatuses.PLAYING            

    elif game_status == GameStatuses.MENU:
        clean_screen(screen, game_status)
        menu.draw(screen)
        events = pygame.event.get()
        if check_exit(events):
            pygame.quit()
            exit(0)
        user_choice = menu.get_user_choice(events)
        if user_choice is not None:
            if user_choice == UserChoicesMenu.PLAY:
                game_status = GameStatuses.PLAYING
                entities, obstacles = start_new_game(entities, obstacles)
            elif user_choice == UserChoicesMenu.EXIT:
                pygame.quit()
                exit(0)
            elif user_choice == UserChoicesMenu.ABOUT:
                webbrowser.open(ABOUT_URL)

    elif game_status == GameStatuses.PLAYING:
        events = pygame.event.get()
        if check_pause(events):
            game_status = GameStatuses.PAUSE
            continue
        if check_exit(events):
            pygame.quit()
            exit(0)
        clean_screen(screen, GameStatuses.PLAYING)
        add_obstacle_if_necessary(entities, obstacles)
        for entity in entities:
            if entity.is_movable:
                entity.move(
                    time_passed_in_secs,
                    up_button_clicked=up_button_clicked(events)
                )
            if entity.can_die:
                dead = entity.try_to_die(obstacles)
                if dead:
                    entity.draw(screen)
                    pygame.display.flip()
                    game_status = GameStatuses.GAME_OVER
                    break
            if entity.must_be_deleted:
                entity.delete()
            else:
                entity.draw(screen)
    pygame.display.flip()
