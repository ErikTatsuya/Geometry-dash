import pygame
from scenes.base import Scene
from settings import *
from world.level import Level

class GameScene(Scene):
    def __init__(self, manager, level_path):
        super().__init__(manager)

        print("GameScene:", level_path)

        self.level = Level(level_path)

        print("Objetos:", len(self.level.objects))

        # background vindo do metadata
        self.bg_image = None

        bg_path = self.level.metadata.get("background")

        if bg_path:
            full_path = ASSETS_DIR / bg_path
            self.bg_image = pygame.image.load(str(full_path)).convert()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.main_levels import MainLevelsScene
                    self.manager.set_scene(MainLevelsScene(self.manager))

    def update(self):
        self.level.update()

    def draw(self, screen):
        screen.fill(BLACK)

        # background primeiro
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))

        # objetos depois
        for obj in self.level.objects:
            obj.draw(screen)