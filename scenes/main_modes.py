import pygame
from scenes.base import Scene
from scenes.button import Button
from settings import *

class MainModesScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 50)

        # caixa (container)
        self.box_rect = pygame.Rect(150, 200, 500, 180)

        # botão centralizado dentro da caixa
        self.btn_main_levels = Button(
            (MIDDLE_X - 150, self.box_rect.centery - 30, 300, 60),
            "Main Levels",
            self.font
        )

        # força estilo do botão
        self.btn_main_levels.color_idle = GREEN
        self.btn_main_levels.color_hover = (0, 200, 0)

    def handle_events(self, events):
        for event in events:

            if self.btn_main_levels.is_clicked(event):
                from scenes.main_levels import MainLevelsScene
                self.manager.set_scene(MainLevelsScene(self.manager))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.main_menu import MainMenuScene
                    self.manager.set_scene(MainMenuScene(self.manager))

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # título
        title_surf = self.font.render("Main Modes", True, WHITE)
        title_rect = title_surf.get_rect(center=(MIDDLE_X, 120))
        screen.blit(title_surf, title_rect)

        # caixa
        pygame.draw.rect(screen, (30, 30, 30), self.box_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.box_rect, 2, border_radius=10)

        # desenhar botão
        self.btn_main_levels.draw(screen)

        # garantir borda branca no botão (caso Button não tenha)
        pygame.draw.rect(screen, WHITE, self.btn_main_levels.rect, 2, border_radius=10)

        # voltar
        back_surf = self.font.render("ESC - Back", True, WHITE)
        back_rect = back_surf.get_rect(center=(MIDDLE_X, 500))
        screen.blit(back_surf, back_rect)