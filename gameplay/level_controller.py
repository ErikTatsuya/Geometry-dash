import pygame
from gameplay.player.player import Player
from settings import *

class LevelController:
    def __init__(self, level):

        self.level = level

        self.camera_x = 0

        self.bg_image = None

        bg_path = self.level.metadata.get("background")

        if bg_path:
            full_path = ASSETS_DIR / bg_path
            self.bg_image = pygame.image.load(str(full_path)).convert()

        self.player = Player(START_POS)

    def update(self):

        solids = self.level.get_solids()

        self.player.update(solids)

        target_x = self.player.x - 200
        self.camera_x += (target_x - self.camera_x) * 0.1

        self.level.update()

    def draw(self, screen):

        screen.fill(BLACK)

        if self.bg_image:
            screen.blit(self.bg_image, (-self.camera_x * 0.3, 0))

        for obj in self.level.objects:
            obj.draw(screen, self.camera_x)

        self.player.draw(screen, self.camera_x)