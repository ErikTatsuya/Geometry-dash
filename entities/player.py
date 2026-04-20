import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = IMAGES['cube']
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=(100, 450))
        
        # Física
        self.vel_y = 0
        self.gravity_dir = 1 # 1 normal, -1 invertida
        self.on_ground = False
        self.mode = "cube" # cube, ship, wave
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        jump_input = keys[pygame.K_SPACE] or keys[pygame.K_UP] or mouse[0]

        # Gravidade e Pulo
        if self.mode == "cube":
            if self.on_ground and jump_input:
                self.vel_y = -8 * self.gravity_dir
                self.on_ground = False
            
            self.vel_y += GRAVITY * self.gravity_dir
            self.rect.y += self.vel_y

            # Rotação do Cubo (Corrigida para não pulsar)
            if not self.on_ground:
                self.angle -= 6 * self.gravity_dir
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                # Alinha o cubo ao chão
                self.angle = 0
                self.image = self.original_image
                self.rect = self.image.get_rect(center=self.rect.center)

        elif self.mode == "ship":
            if jump_input:
                self.vel_y -= 0.5 * self.gravity_dir
            else:
                self.vel_y += 0.3 * self.gravity_dir
            
            # Limite de velocidade da nave
            self.vel_y = max(-6, min(6, self.vel_y))
            self.rect.y += self.vel_y
            
            # Inclinação da nave
            self.angle = -self.vel_y * 4
            self.image = pygame.transform.rotate(IMAGES['ship'], self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        self.on_ground = False # Reset para checagem de colisão no main