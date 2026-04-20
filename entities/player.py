import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.mode = "cube"
        self.image = IMAGES['cube']
        self.rect = self.image.get_rect(topleft=(100, 450))
        self.vel_y = 0
        self.gravity_dir = 1
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        clicked = keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]

        if self.mode == "cube":
            self.vel_y += GRAVITY * self.gravity_dir
            if clicked and self.on_ground:
                self.vel_y = -9 * self.gravity_dir
                self.on_ground = False
            self.image = IMAGES['cube']

        elif self.mode == "ship":
            self.vel_y += (GRAVITY * 0.4) * self.gravity_dir
            if clicked:
                self.vel_y -= 0.7 * self.gravity_dir
            self.image = IMAGES['ship']

        elif self.mode == "wave":
            speed = 6 * self.gravity_dir
            self.vel_y = -speed if clicked else speed
            self.image = IMAGES['wave']

        # Limitar velocidade terminal
        terminal_speed = 15
        if abs(self.vel_y) > terminal_speed:
            if self.vel_y > 0:
                self.vel_y = terminal_speed
            else:
                self.vel_y = -terminal_speed
            
        self.rect.y += self.vel_y
        self.on_ground = False