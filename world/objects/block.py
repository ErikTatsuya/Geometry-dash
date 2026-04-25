import pygame
from settings import TILE_SIZE, ASSETS_DIR

class Block:
    def __init__(self, grid_x, grid_y, image_path, rotation=0):

        self.x = grid_x * TILE_SIZE
        self.y = grid_y * TILE_SIZE

        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

        full_path = ASSETS_DIR / image_path

        self.image = pygame.image.load(str(full_path)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

        self.rotation = rotation

    def update(self):
        pass

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))