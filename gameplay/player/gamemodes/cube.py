import pygame
from settings import *
from world.grid import GRID_SIZE
from .base import BaseMode

class CubeMode(BaseMode):
    def __init__(self, player):
        self.player = player

        self.mini = False
        self.gravity = 1
        self.size = GRID_SIZE

        self.velocity_y = 0

        self.image = pygame.image.load(
            ASSETS_DIR / "objects/player/cube/cube_1.png"
        ).convert_alpha()

        self.scaled_image = self.image

        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.danger_hitbox = pygame.Rect(0, 0, 0, 0)

    def update_size(self):
        if self.mini:
            self.size = int(GRID_SIZE * 0.6)
        else:
            self.size = GRID_SIZE

        self.scaled_image = pygame.transform.scale(
            self.image, (self.size, self.size)
        )

    def update(self, solids):
        self.update_size()

        # física básica
        self.velocity_y += self.gravity
        self.player.y += self.velocity_y

        x = self.player.x
        y = self.player.y

        # hitbox principal
        self.hitbox.topleft = (x, y)

        # hitbox de perigo (menor)
        shrink = int(self.size * 0.15)

        self.danger_hitbox = pygame.Rect(
            x + shrink,
            y + shrink,
            self.size - shrink * 2,
            self.size - shrink * 2
        )

        # colisão simples com chão
        for obj in solids:
            if self.hitbox.colliderect(obj.rect):
                if self.velocity_y > 0:
                    self.player.y = obj.rect.top - self.size
                    self.velocity_y = 0

    def draw(self, screen, camera_x):
        screen.blit(
            self.scaled_image,
            (self.player.x - camera_x, self.player.y)
        )