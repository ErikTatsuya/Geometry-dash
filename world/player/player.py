import pygame

class Player:
    def __init__(self, x, y, gamemode):
        self.x = x
        self.y = y

        self.gamemode = gamemode
        self.gamemode.attach(self)

    def set_gamemode(self, gamemode):
        self.gamemode = gamemode
        self.gamemode.attach(self)

    def update(self):
        self.gamemode.update()

    @property
    def hitbox(self):
        return self.gamemode.hitbox

    @property
    def danger_hitbox(self):
        return self.gamemode.danger_hitbox