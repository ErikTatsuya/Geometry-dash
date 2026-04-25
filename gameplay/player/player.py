from gameplay.player.gamemodes.cube import CubeMode
from settings import *


class Player:
    def __init__(self, grid_pos):

        self.x = grid_pos[0] * TILE_SIZE
        self.y = grid_pos[1] * TILE_SIZE

        # gamemode ativo
        self.mode = CubeMode(self)

    def update(self, solids):
        self.mode.update(solids)

    def draw(self, screen, camera_x):
        self.mode.draw(screen, camera_x)