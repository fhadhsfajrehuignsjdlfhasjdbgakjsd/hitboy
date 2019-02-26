from helpers import *
import pygame
from datetime import datetime
import time
from consts import *
from random import choice, uniform, randint
import threading
from helpers import get_max_score, set_max_score


class GameObject(object):
    '''base object for all base objects'''
    can_finish_game = False
    is_movable = False
    must_die = False
    can_die = False
    can_be_destroyed_by_rockets = False

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def coords(self):
        return (self.x, self.y)

    def draw(self, screen):
        pass

    def move(
        self,
        time_passed_in_secs: int,
        **kwargs
    ):
        pass

    def update_rect(self):
        pass
    
    def delete(self, entities, obstacles, planes, rockets):
        if self in entities:
            entities.remove(self)
        if self in obstacles:
            obstacles.remove(self)
        if self in rockets:
            rockets.remove(self)
        if self in planes:
            planes.remove(self)
        del self

    def die(self, entities, obstacles, planes, rockets):
        self.delete(entities, obstacles, planes, rockets)


class Floor(GameObject):
    '''element hitboy runs on'''
    is_movable = False
    can_kill_hitboy = False

    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(
            *FLOOR_RECT_POSITION
        )

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)


class Hitboy(GameObject):
    '''represents our character and his score'''
    can_die = True
    is_movable = True  # character moves upside down
    y_speed, jump_speed = 0, -600  # pix per second
    can_kill_hitboy = False
    dead = False

    images = [
        pygame.transform.scale(image, HITBOY_SIZE) for image in (
            load_image('hitboy0.png'),
            load_image('hitboy1.png')
        )
    ]

    dead_image = pygame.transform.scale(
        load_image('hitboy_dead.png'), DEAD_HITBOY_SIZE
    )

    def __init__(self, x: int, y: int, floor: Floor):
        super().__init__(x, y)
        self.update_rect()
        self.current_image_index = 0
        self.floor = floor
        self.weapon = Weapon(*WEAPON_INITIAL_POSITION)

    def update_rect(self):
        if not self.dead:
            self.rect = pygame.Rect(
                self.x,
                self.y,
                HITBOY_SIZE[0],
                HITBOY_SIZE[1]
            )
        else:
            self.rect = pygame.Rect(
                self.x,
                self.y,
                DEAD_HITBOY_SIZE[0],
                DEAD_HITBOY_SIZE[1]
            )

    def move(
        self,
        time_passed_in_secs: int,
        **kwargs
    ):
        if not (datetime.now().microsecond % CHANGE_IMAGE_PERIOD):
            self.change_image()
        if self.stands_on_floor():
            if kwargs.get('up_button_clicked', False):
                self.y_speed = self.jump_speed  # self.jump
            else:
                self.put_hero_on_the_ground()
                self.weapon.put_weapon_on_the_ground()
                self.y_speed = 0
        else:
            self.y_speed += G * time_passed_in_secs
        self.y += int(self.y_speed * time_passed_in_secs)
        self.weapon.y += int(self.y_speed * time_passed_in_secs)
        self.update_rect()
        self.weapon.update_rect()

    def put_hero_on_the_ground(self):
        self.x, self.y = HITBOY_START_POSITION
        self.update_rect()

    def stands_on_floor(self) -> bool:
        return self.rect.colliderect(self.floor.rect)

    def draw(self, screen):
        if not self.dead:
            screen.blit(self.images[self.current_image_index], self.rect)
        else:
            screen.blit(self.dead_image, self.rect)

    def __str__(self):
        return "Hitboy! x: {}, y: {}, current_image: {}, y_speed: {}".format(
            self.x,
            self.y,
            self.current_image_index,
            self.y_speed
        )

    def change_image(self):
        self.current_image_index = (
            self.current_image_index + 1) % len(self.images)

    def try_to_die(self, obstacles) -> bool:
        for obstacle in obstacles:
            if obstacle.rect.colliderect(self.rect):
                self.dead = True
                self.y = DEAD_HITBOY_Y_POSITION
                self.update_rect()
                return self.dead
        return False


class Weapon(GameObject):
    # weapon is not movable, it moves with hitboy

    def __init__(self, x, y):
        super().__init__(x, y)
        self.orig_image = pygame.transform.scale(
            load_image('launcher.png'), WEAPON_SIZE
        )
        self.angle = 0
        self.image = self.orig_image
        self.update_rect()
        
    def get_rocket_initial_point(self):
        x, y = self.image.get_rect()[2:]
        return (self.x + 20, self.y + 20)

    def rotate(self, angle):
        angle = min(120, angle)
        self.angle = angle
        self.image = pygame.transform.rotate(self.orig_image, angle)
        self.update_rect()

    def put_weapon_on_the_ground(self):
        self.x, self.y = WEAPON_INITIAL_POSITION
        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(
            self.x,
            self.y,
            WEAPON_SIZE[0],
            WEAPON_SIZE[1]
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Obstacle(GameObject):
    is_movable = True

    def __init__(self, x, y, speed):
        image_name = choice(OBSTACLE_IMAGES_NAMES)
        super().__init__(x, y)
        self.image = pygame.transform.scale(
            load_image(image_name), OBSTACLE_SIZE
        )
        self.update_rect()
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, time_passed_in_secs, **kwargs):
        self.x += self.speed * time_passed_in_secs
        if self.x <= 0 - OBSTACLE_SIZE[0]:
            self.must_die = True
        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(
            self.x,
            self.y,
            OBSTACLE_SIZE[0],
            OBSTACLE_SIZE[1]
        )


class Plane(GameObject):
    is_movable = True   
    can_be_destroyed_by_rockets = True
    can_finish_game = True
    destroyed_image = pygame.transform.scale(
        load_image('boom.png'),
        PLANE_SIZE
    )

    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.image = pygame.transform.scale(
            load_image('plane.png'), PLANE_SIZE)
        self.update_rect()
        self.update_mesh()
        self.speed = speed
        self.destroyed = False
        self.destroyed_time = None
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def try_to_finish_game(self) -> bool:
        return (not self.destroyed) and self.x <= 0 - PLANE_SIZE[0]

    def move(self, time_passed_in_secs, **kwargs):
        if not self.destroyed:
            self.x += self.speed * time_passed_in_secs
            self.update_rect()
            self.update_mesh()

    def update_mesh(self):
        self.mesh = pygame.Rect(
            self.x + 10,
            self.y + 10,
            PLANE_SIZE[0] - 20,
            PLANE_SIZE[1] - 20
        )
    
    def collides_rocket(self, rocket):
        return self.mesh.colliderect(rocket.mesh)

    def update_rect(self):
        self.rect = pygame.Rect(
            self.x,
            self.y,
            PLANE_SIZE[0],
            PLANE_SIZE[1]
        )

    def die(self, entities, obstacles, planes, rockets):
        self.image = self.destroyed_image
        print(time.time() - self.destroyed_time)
        if time.time() - self.destroyed_time >= 1.0:
            self.delete(entities, obstacles, planes, rockets)

    def try_to_become_destroyed(self, entities, obstacles, planes, rockets):
        if not self.destroyed:
            for rocket in rockets:
                if self.collides_rocket(rocket):
                    self.destroyed_time = time.time()
                    self.destroyed = True
                    self.must_die = True
                    rocket.delete(entities, obstacles, planes, rockets)
                    self.die(entities, obstacles, planes, rockets)


class Rocket(GameObject):
    is_movable = True

    def __init__(self, x, y, k, b, rotation_angle):
        # y = kx
        self.image = pygame.transform.rotate(
            pygame.transform.scale(load_image('rocket.png'), ROCKET_SIZE),
            rotation_angle    
        )
        super().__init__(x, y)
        self.k, self.b = k, b
        self.x_speed = get_rocket_speed_by_angle(rotation_angle)
        self.update_rect()
        self.update_mesh()
        self.rotation_angle = rotation_angle
    
    def update_rect(self):
        self.rect = pygame.Rect(
            self.x,
            self.y,
            ROCKET_SIZE[0],
            ROCKET_SIZE[1]
        )

    def update_mesh(self):
        self.mesh = pygame.Rect(
            self.x,
            self.y,
            ROCKET_SIZE[0],
            ROCKET_SIZE[1]
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, time_passed_in_secs, **kwargs):
        self.x += self.x_speed * time_passed_in_secs
        self.y = self.x * self.k + self.b
        if ((self.x <= 0 - ROCKET_SIZE[0]) or (self.y <= 0 - ROCKET_SIZE[1])):
            self.must_die = True
        self.update_rect()
        self.update_mesh()


# score is not game object
class Score(object):

    def __init__(self):
        self.max_score = get_max_score()
        self.font = pygame.font.Font('fonts/Roboto-Black.ttf', 25)
        self.reset_score()
    
    def check_new_max_score(self):
        if self.current_score >= self.max_score:
            self.max_score = self.current_score
            set_max_score(self.max_score)

    def reset_score(self):
        self.current_score = 0

    def increase(self):
        self.current_score += 0.1
    
    def draw(self, screen):
        screen.blit(
                self.font.render(str(int(self.current_score)), True, BLACK),
                SCORE_INITIAL_POSITION
            )
        screen.blit(
            self.font.render('Max: ' + str(int(self.max_score)), True, BLACK),
            MAX_SCORE_INITIAL_POSITION
        )


#  menu is not game object
class Menu(object):

    def __init__(self, game_status: int):
        self.game_status = game_status
        self.play_item_rect = pygame.Rect(*MENU_PLAY_ITEM_POSITION)
        if self.game_status == GameStatuses.MENU:
            self.about_item_rect = pygame.Rect(*MENU_ABOUT_ITEM_POSITION)
        else:
            self.restart_item_rect = pygame.Rect(*MENU_RESTART_ITEM_POSITION)            
        self.exit_item_rect = pygame.Rect(*MENU_EXIT_ITEM_POSITION)
        self.font = pygame.font.Font('fonts/Roboto-Black.ttf', 50)

    def get_user_choice(self, events):
        if check_pause(events):
            return UserChoicesMenu.PLAY
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.play_item_rect.collidepoint(pos):
                    return UserChoicesMenu.PLAY
                elif self.exit_item_rect.collidepoint(pos):
                    return UserChoicesMenu.EXIT
                if self.game_status == GameStatuses.MENU:
                    if self.about_item_rect.collidepoint(pos):
                        return UserChoicesMenu.ABOUT
                else:
                    if self.restart_item_rect.collidepoint(pos):
                        return UserChoicesMenu.RESTART
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.play_item_rect, 2)
        if self.game_status == GameStatuses.MENU:
            screen.blit(
                self.font.render('Play', True, BLACK),
                tuple(map(lambda x: x + 25, MENU_PLAY_ITEM_POSITION[:2]))
            )
            pygame.draw.rect(screen, BLACK, self.about_item_rect, 2)
            screen.blit(
                self.font.render('About', True, BLACK),
                tuple(map(lambda x: x + 25, MENU_ABOUT_ITEM_POSITION[:2]))
            )
        else:
            screen.blit(
                self.font.render('Continue', True, BLACK),
                tuple(map(lambda x: x + 25, MENU_PLAY_ITEM_POSITION[:2]))
            )
            pygame.draw.rect(screen, BLACK, self.restart_item_rect, 2)
            screen.blit(
                self.font.render('Restart', True, BLACK),
                tuple(map(lambda x: x + 25, MENU_RESTART_ITEM_POSITION[:2]))
            )
        
        pygame.draw.rect(screen, BLACK, self.exit_item_rect, 2)
        screen.blit(
            self.font.render('Exit', True, BLACK),
            tuple(map(lambda x: x + 25, MENU_EXIT_ITEM_POSITION[:2]))
        )


# responsible for adding objects
class ObjectAdder(object):

    def __init__(self, *args, **kwargs):
        self.reset_everything()

    def reset_everything(self):
        self.reset_obstacle_timer()
        self.reset_plane_timer()
        self.reset_shoot_timer()
        self.reset_tbno()
        self.reset_tbnp()
        self.reset_soo()
        self.reset_sop()

    def reset_obstacle_timer(self):
        self.obstacle_timer = time.time()
    
    def reset_shoot_timer(self):
        self.shoot_timer = time.time()
    
    def reset_plane_timer(self):
        self.plane_timer = time.time()

    def reset_timers(self):
        self.reset_obstacle_timer()
        self.reset_plane_timer()
        self.reset_shoot_timer()

    def reset_tbno(self):
        self.time_before_next_obstacle = uniform(0.45, 0.9)

    def reset_tbnp(self):
        self.time_before_next_plane = uniform(1.9, 2.5)

    def reset_sop(self):
        self.speed_of_plane = -100

    def reset_soo(self):
        self.speed_of_obstacle = -500

    def add_planes_and_obstacles_if_necessary(
            self, entities, obstacles, planes):
        self.add_obstacle_if_necessary(entities, obstacles)
        self.add_plane_if_necessary(entities, planes)

    def add_obstacle_if_necessary(self, entities, obstacles):
        if time.time() - self.obstacle_timer >= self.time_before_next_obstacle:
            self.reset_obstacle_timer()
            self.reset_tbno()
            obstacle = Obstacle(
                *OBSTACLE_START_POSITION, self.speed_of_obstacle)
            self.speed_of_obstacle -= 2
            obstacles.append(obstacle)
            entities.append(obstacle)

    def add_plane_if_necessary(self, entities, planes):
        if time.time() - self.plane_timer >= self.time_before_next_plane:
            self.reset_plane_timer()
            self.reset_tbnp()
            plane = Plane(
                PLANE_INITIAL_X_POSITION,
                randint(*PLANE_Y_POSITION_RANGE),
                self.speed_of_plane
            )
            self.speed_of_plane -= 5
            entities.append(plane)
            planes.append(plane)

    def add_rockets_if_necessary(self, entities, rockets, rocket_start_pos, position):
        if position == (-1, -1):
            return
        if time.time() - self.shoot_timer >= 1.0:  # we can shoot once per second
            k, b = find_k_and_b(*position, *rocket_start_pos)
            if k is None and b is None:
                return
            r_a = get_angle_by_three_points(
                (rocket_start_pos[0] + 1, rocket_start_pos[1]),
                rocket_start_pos,
                position,
            )
            rocket = Rocket(*rocket_start_pos, k, b, r_a)
            entities.append(rocket)
            rockets.append(rocket)
            self.reset_shoot_timer()


menu = Menu(GameStatuses.MENU)
pause_menu = Menu(GameStatuses.PAUSE)
object_adder = ObjectAdder()
score = Score()
entities = []  # all game objects
obstacles = []  # all objects that can kill hero
planes = []
rockets = []


def start_new_game(entities, obstacles, obstacle_adder, score):
    obstacle_adder.reset_everything()
    score.reset_score()
    entities = []  # all game objects
    obstacles = []  # things that can kill hitboy
    planes = []
    rockets = []
    entities.append(
        Floor(*FLOOR_RECT_POSITION[:2])
    )
    entities.append(
        Hitboy(*HITBOY_START_POSITION, entities[0])
    )
    entities.append(
        entities[-1].weapon
    )

    return entities, obstacles
