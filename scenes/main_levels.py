import pygame
from scenes.base import Scene
from settings import *
from level_loader import load_levels

class MainLevelsScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        self.font = pygame.font.SysFont(None, 50)
        self.small_font = pygame.font.SysFont(None, 35)

        # caixa onde os níveis ficam
        self.box_rect = pygame.Rect(150, 180, 500, 260)

        # carregar níveis
        self.levels = load_levels(MAIN_LEVELS)

        # lista de botões
        self.buttons = []
        y = self.box_rect.top + 30

        for level in self.levels:
            name = level["data"]["metadata"]["name"]

            rect = pygame.Rect(self.box_rect.left + 50, y, 400, 40)

            self.buttons.append({
                "rect": rect,
                "text": name,
                "level": level
            })

            y += 55

    def handle_events(self, events):
        for event in events:

            # voltar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.main_modes import MainModesScene
                    self.manager.set_scene(MainModesScene(self.manager))

            # clique
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        from scenes.level_info import LevelInfoScene
                        self.manager.set_scene(LevelInfoScene(self.manager, btn["level"]))

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # título
        title_surf = self.font.render("Main Levels", True, WHITE)
        title_rect = title_surf.get_rect(center=(MIDDLE_X, 120))
        screen.blit(title_surf, title_rect)

        # caixa (container)
        pygame.draw.rect(screen, (30, 30, 30), self.box_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.box_rect, 2, border_radius=10)

        mouse_pos = pygame.mouse.get_pos()

        # botões
        for btn in self.buttons:
            rect = btn["rect"]

            # hover
            if rect.collidepoint(mouse_pos):
                color = (0, 200, 0)  # verde mais claro
            else:
                color = GREEN

            # fundo do botão
            pygame.draw.rect(screen, color, rect, border_radius=8)

            # borda branca
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)

            # texto centralizado
            text_surf = self.small_font.render(btn["text"], True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)

            screen.blit(text_surf, text_rect)

        # voltar
        back_surf = self.font.render("ESC - Back", True, WHITE)
        back_rect = back_surf.get_rect(center=(MIDDLE_X, 520))
        screen.blit(back_surf, back_rect)