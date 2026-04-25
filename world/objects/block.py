import pygame
from settings import *
from world.grid import grid_to_world, GRID_SIZE

class Block:
    def __init__(self, x, y, rotation=0):
        self.grid_x = x
        self.grid_y = y
        self.rotation = rotation

        # posição em pixels
        self.x, self.y = grid_to_world(x, y)

        # hitbox sólida
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def update(self):
        pass