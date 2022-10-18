import pygame
from abc import ABC, abstractmethod


class Unit(pygame.sprite.Sprite, ABC):
    D_UP = "up"
    D_DOWN = "down"
    D_LEFT = "left"
    D_RIGHT = "right"
    D_STOP = "stop"

    def __init__(self, coordinates):
        super(Unit, self).__init__()
        self.__init_surf__()
        self.init_x, self.init_y = coordinates
        self.rect.x, self.rect.y = coordinates
        self.prev_x, self.prev_y = coordinates
        self.direction = self.D_STOP

    @abstractmethod
    def __init_surf__(self):
        pass


class Tank(Unit):
    def __init__(self, coordinates, towed=False):
        super(Tank, self).__init__(coordinates)
        self.towed = towed

    def __init_surf__(self):
        self.surfaces = {
            self.D_STOP: pygame.image.load("./img/tank_up.png").convert_alpha(),
            self.D_UP: pygame.image.load("./img/tank_up.png").convert_alpha(),
            self.D_DOWN: pygame.image.load("./img/tank_down.png").convert_alpha(),
            self.D_LEFT: pygame.image.load("./img/tank_left.png").convert_alpha(),
            self.D_RIGHT: pygame.image.load("./img/tank_right.png").convert_alpha(),
        }
        self.surf = self.surf = self.surfaces[self.D_UP]
        self.rect = self.surf.get_rect()

    def update(self):
        if self.prev_y < self.rect.y:
            self.surf = self.surf = self.surfaces[self.D_UP]
        if self.prev_y > self.rect.y:
            self.surf = self.surf = self.surfaces[self.D_DOWN]
        if self.prev_x < self.rect.x:
            self.surf = self.surf = self.surfaces[self.D_LEFT]
        if self.prev_x > self.rect.x:
            self.surf = self.surf = self.surfaces[self.D_RIGHT]


class Tractor(Unit):
    def __init__(self, coordinates):
        super(Tractor, self).__init__(coordinates)
        self.towed_tanks = pygame.sprite.Group()

    def __init_surf__(self):
        self.surfaces = {
            self.D_STOP: pygame.image.load("./img/tractor_up.png").convert_alpha(),
            self.D_UP: pygame.image.load("./img/tractor_up.png").convert_alpha(),
            self.D_DOWN: pygame.image.load("./img/tractor_down.png").convert_alpha(),
            self.D_LEFT: pygame.image.load("./img/tractor_left.png").convert_alpha(),
            self.D_RIGHT: pygame.image.load("./img/tractor_right.png").convert_alpha(),
        }
        self.surf = self.surfaces[self.D_UP]
        self.rect = self.surf.get_rect()

    def add_towed_tank(self, tank: Tank):
        tank.towed = True
        self.towed_tanks.add(tank)

    def reset(self):
        self.direction = self.D_STOP
        self.rect.x = self.init_x
        self.rect.y = self.init_y
        self.towed_tanks.empty()

    def set_direction(self, direction):
        self.direction = direction

    def update(self):
        if self.direction == self.D_UP:
            self.surf = self.surfaces[self.D_UP]
            self.prev_x = self.rect.x
            self.prev_y = self.rect.y
            self.rect.move_ip(0, -32)
        if self.direction == self.D_DOWN:
            self.surf = self.surfaces[self.D_DOWN]
            self.prev_x = self.rect.x
            self.prev_y = self.rect.y
            self.rect.move_ip(0, 32)
        if self.direction == self.D_LEFT:
            self.surf = self.surfaces[self.D_LEFT]
            self.prev_x = self.rect.x
            self.prev_y = self.rect.y
            self.rect.move_ip(-32, 0)
        if self.direction == self.D_RIGHT:
            self.prev_x = self.rect.x
            self.prev_y = self.rect.y
            self.surf = self.surfaces[self.D_RIGHT]
            self.rect.move_ip(32, 0)

        prev_tank = None
        for tank in self.towed_tanks:
            tank.prev_x = tank.rect.x
            tank.prev_y = tank.rect.y

            if isinstance(prev_tank, Tank):
                tank.rect.x = prev_tank.prev_x
                tank.rect.y = prev_tank.prev_y
            else:
                tank.rect.x = self.prev_x
                tank.rect.y = self.prev_y

            prev_tank = tank

            tank.update()
