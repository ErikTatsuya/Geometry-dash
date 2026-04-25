import pygame
from scenes.base import Scene
from settings import *

class LevelInfoScene(Scene):
    def __init__(self, manager, level):
        super().__init__(manager)

        self.font = pygame.font.SysFont(None, 50)
        self.small_font = pygame.font.SysFont(None, 35)

        # dados do level
        self.level_path = level["path"]
        self.metadata = level["data"]["metadata"]

        # caixa central
        self.box_rect = pygame.Rect(150, 160, 500, 300)

        # botão PLAY
        self.play_button = pygame.Rect(MIDDLE_X - 100, 380, 200, 50)

    def handle_events(self, events):
        for event in events:

            # voltar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.main_levels import MainLevelsScene
                    self.manager.set_scene(MainLevelsScene(self.manager))

            # clicar PLAY
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.play_button.collidepoint(event.pos):
                    from scenes.game_scene import GameScene
                    self.manager.set_scene(GameScene(self.manager, self.level_path))

    def draw(self, screen):
        screen.fill(BLACK)

        # título
        title_surf = self.font.render(self.metadata["name"], True, WHITE)
        title_rect = title_surf.get_rect(center=(MIDDLE_X, 100))
        screen.blit(title_surf, title_rect)

        # caixa
        pygame.draw.rect(screen, (30, 30, 30), self.box_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.box_rect, 2, border_radius=10)

        # infos
        y = self.box_rect.top + 40

        lines = [
            f"Desc: {self.metadata['description']}",
            f"Best: {self.metadata['best_run']}",
            f"Difficulty: {self.metadata['dificulty']}"
        ]

        for line in lines:
            surf = self.small_font.render(line, True, WHITE)
            rect = surf.get_rect(center=(MIDDLE_X, y))
            screen.blit(surf, rect)
            y += 50

        # botão PLAY (hover)
        mouse_pos = pygame.mouse.get_pos()

        if self.play_button.collidepoint(mouse_pos):
            color = (0, 200, 0)
        else:
            color = GREEN

        pygame.draw.rect(screen, color, self.play_button, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.play_button, 2, border_radius=8)

        play_surf = self.small_font.render("PLAY", True, WHITE)
        play_rect = play_surf.get_rect(center=self.play_button.center)
        screen.blit(play_surf, play_rect)

        # voltar
        back_surf = self.font.render("ESC - Back", True, WHITE)
        back_rect = back_surf.get_rect(center=(MIDDLE_X, 520))
        screen.blit(back_surf, back_rect)