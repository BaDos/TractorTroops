import pygame


class Tractor(pygame.sprite.Sprite):
    D_UP = "up"
    D_DOWN = "down"
    D_LEFT = "left"
    D_RIGHT = "right"
    D_STOP = "stop"

    def __init__(self, init_x, init_y):
        super(Tractor, self).__init__()
        self.surfaces = {
            self.D_STOP: pygame.image.load("./img/tractor_up.png").convert_alpha(),
            self.D_UP: pygame.image.load("./img/tractor_up.png").convert_alpha(),
            self.D_DOWN: pygame.image.load("./img/tractor_down.png").convert_alpha(),
            self.D_LEFT: pygame.image.load("./img/tractor_left.png").convert_alpha(),
            self.D_RIGHT: pygame.image.load("./img/tractor_right.png").convert_alpha(),
        }
        self.surf = pygame.image.load("./img/tractor_up.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.init_x = init_x
        self.init_y = init_y
        self.rect.x = init_x
        self.rect.y = init_y
        self.direction = self.D_STOP

    def reset(self):
        self.direction = self.D_STOP
        self.rect.x = self.init_x
        self.rect.y = self.init_y

    def set_direction(self, direction):
        self.direction = direction

    def update(self):
        if self.direction == self.D_UP:
            self.surf = self.surfaces[self.D_UP]
            self.rect.move_ip(0, -32)
        if self.direction == self.D_DOWN:
            self.surf = self.surfaces[self.D_DOWN]
            self.rect.move_ip(0, 32)
        if self.direction == self.D_LEFT:
            self.surf = self.surfaces[self.D_LEFT]
            self.rect.move_ip(-32, 0)
        if self.direction == self.D_RIGHT:
            self.surf = self.surfaces[self.D_RIGHT]
            self.rect.move_ip(32, 0)
