import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_q,
    K_c,
    KEYDOWN,
    QUIT,
)

from game.unit import Tractor, Tank


class TractorTroops:
    SCREEN_WIDTH = 768
    SCREEN_HEIGHT = 640

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tractor Troops")
        ico = pygame.image.load("./img/tractor_up.png")
        pygame.display.set_icon(ico)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.tractor = Tractor((self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2))
        self.tank = self.create_tank()
        self.running = True
        self.score = 0

    def run(self):
        while self.running:
            self.clock.tick(5 + 1 * self.score)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = self.show_quit_screen(True)
                    if event.key == K_UP:
                        self.tractor.set_direction(Tractor.D_UP)
                    if event.key == K_DOWN:
                        self.tractor.set_direction(Tractor.D_DOWN)
                    if event.key == K_LEFT:
                        self.tractor.set_direction(Tractor.D_LEFT)
                    if event.key == K_RIGHT:
                        self.tractor.set_direction(Tractor.D_RIGHT)
                elif event.type == QUIT:
                    self.running = self.show_quit_screen(True)

            bg = pygame.image.load("./img/field.png").convert()
            self.screen.blit(bg, (0, 0))

            self.tractor.update()
            self.screen.blit(self.tractor.surf, self.tractor.rect)
            self.screen.blit(self.tank.surf, self.tank.rect)
            for tank in self.tractor.towed_tanks:
                self.screen.blit(tank.surf, tank.rect)

            pygame.display.flip()

            if self.is_bad_collision():
                self.running = self.show_quit_screen()

            if self.is_good_collision():
                self.tractor.add_towed_tank(self.tank)
                self.tank = self.create_tank()
                self.score += 1

        self.quit()

    def is_bad_collision(self):
        if self.tractor.rect.left < 0:
            return True
        if self.tractor.rect.right > self.SCREEN_WIDTH:
            return True
        if self.tractor.rect.top < 0:
            return True
        if self.tractor.rect.bottom > self.SCREEN_HEIGHT:
            return True
        if pygame.sprite.spritecollideany(self.tractor, self.tractor.towed_tanks):
            return True

        return False

    def is_good_collision(self):
        return self.tank.rect.colliderect(self.tractor.rect)

    def get_rand_coordinates(self):
        return (
            random.randint(0, 23) * 32,
            random.randint(0, 19) * 32
        )

    def create_tank(self):
        tank = Tank(self.get_rand_coordinates())

        while pygame.sprite.spritecollideany(tank, self.tractor.towed_tanks)\
                or tank.rect.colliderect(self.tractor.rect):
            coordinates = self.get_rand_coordinates()
            tank.rect.x, tank.rect.y = coordinates
            tank.prev_x, tank.prev_y = coordinates

        return tank

    def quit(self):
        pygame.quit()
        quit()

    def reset(self):
        self.score = 0
        self.tractor.reset()

    def show_quit_screen(self, pause=False):
        self.screen.fill((255, 255, 255))
        font_style = pygame.font.SysFont("timesnewroman", 25)

        score = font_style.render("Your score: " + str(self.score), True, (0, 0, 0))
        score_rect = score.get_rect()
        score_rect.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 25)
        self.screen.blit(score, score_rect)

        prompt = font_style.render("Press the key: C - Continue, Q - Quit", True, (0, 0, 0))
        prompt_rect = prompt.get_rect()
        prompt_rect.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 25)
        self.screen.blit(prompt, prompt_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        return False
                    if event.key == K_c:
                        if not pause:
                            self.reset()
                        return True


game = TractorTroops()
game.run()
