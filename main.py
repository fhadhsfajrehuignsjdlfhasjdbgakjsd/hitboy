import pygame
from consts import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

from helpers import *
from entities import entities, obstacles
timer = pygame.time.Clock()
# pygame.mixer.init()
# pygame.mixer.music.load("audio/monster.mp3")
# pygame.mixer.music.play()
game_status = GameStatuses.PLAYING

while True:
    if game_status == GameStatuses.MENU:
        clean_screen(screen, game_status)
        display_menu(screen)
        events = pygame.event.get()
        user_choice = get_user_choice_menu(events)
        if user_choice is not None:
            pass

    if game_status == GameStatuses.PLAYING:
        events = pygame.event.get()
        if check_exit(events):
            pygame.quit()
            exit()
        clean_screen(screen, GameStatuses.PLAYING)
        time_passed_in_secs = timer.tick(60) / 1000
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
                    while True:
                        pass
            if entity.must_be_deleted:
                entity.delete()
            else:
                entity.draw(screen)
        pygame.display.flip()
