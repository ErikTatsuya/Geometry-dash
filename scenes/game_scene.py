import pygame
from scenes.base import Scene
from settings import *
from world.level import Level
from gameplay.level_controller import LevelController

class GameScene(Scene):
    def __init__(self, manager, level_path):
        super().__init__(manager)

        print("GameScene:", level_path)

        self.level = Level(level_path)

        print("Objetos:", len(self.level.objects))

        self.controller = LevelController(self.level)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.main_levels import MainLevelsScene
                    self.manager.set_scene(MainLevelsScene(self.manager))

    def update(self):
        self.controller.update()

    def draw(self, screen):
        screen.fill(BLACK)
        self.controller.draw(screen)