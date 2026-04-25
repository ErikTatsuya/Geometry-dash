import pygame
from scenes.base import Scene

class CustomModesScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 50)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.main_menu import MainMenuScene
                    self.manager.set_scene(MainMenuScene(self.manager))

    def draw(self, screen):
        screen.fill((0, 0, 0))

        text = self.font.render("Custom Modes", True, (255, 255, 255))
        back = self.font.render("ESC - Back", True, (200, 200, 200))

        screen.blit(text, (230, 250))
        screen.blit(back, (230, 320))