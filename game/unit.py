import pygame


class Tractor(pygame.sprite.Sprite):
    D_UP = "up"
    D_DOWN = "down"
    D_LEFT = "left"
    D_RIGHT = "right"
    D_STOP = "stop"

    def __init__(self, init_x, init_y):
        super(Tractor, self).__init__()
        self.surf = pygame.Surface((32, 32))
        self.surf.fill((255, 255, 255))
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
            self.rect.move_ip(0, -32)
        if self.direction == self.D_DOWN:
            self.rect.move_ip(0, 32)
        if self.direction == self.D_LEFT:
            self.rect.move_ip(-32, 0)
        if self.direction == self.D_RIGHT:
            self.rect.move_ip(32, 0)
