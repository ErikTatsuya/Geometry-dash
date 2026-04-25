from player.gamemodes.cube import CubeMode

class Player:
    def __init__(self, x, y):

        self.x = x
        self.y = y

        # gamemode ativo
        self.mode = CubeMode(self)

    def update(self, solids):
        self.mode.update(solids)

    def draw(self, screen, camera_x):
        self.mode.draw(screen, camera_x)