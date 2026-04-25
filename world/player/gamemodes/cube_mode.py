import pygame
from settings import *
from world.grid import GRID_SIZE
from .base_mode import BaseMode

class CubeMode(BaseMode):
    def __init__(self):
        self.mini = False
        self.gravity = 1
        self.size = GRID_SIZE

        self.image = pygame.image.load(
            ASSETS_DIR / "objects/player/cube/cube_1.png"
        ).convert_alpha()

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

    def update(self):
        self.update_size()

        x = self.player.x
        y = self.player.y

        self.hitbox.topleft = (x, y)

        shrink = int(self.size * 0.15)

        self.danger_hitbox = pygame.Rect(
            x + shrink,
            y + shrink,
            self.size - shrink * 2,
            self.size - shrink * 2
        )