import pygame
import math
from scenes.base import Scene
from scenes.custom_modes import CustomModesScene
from scenes.main_modes import MainModesScene
from scenes.button import Button
from settings import *

class MainMenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

        self.font = pygame.font.SysFont(None, 70)
        self.button_font = pygame.font.SysFont(None, 50)

        # containers
        self.title_box = pygame.Rect(150, 80, 500, 120)
        self.menu_box = pygame.Rect(150, 240, 500, 180)

        # botões
        self.btn_main = Button((MIDDLE_X - 150, 270, 300, 60), "Main Modes", self.button_font)
        self.btn_custom = Button((MIDDLE_X - 150, 350, 300, 60), "Custom Modes", self.button_font)

        # estilo botão
        for btn in [self.btn_main, self.btn_custom]:
            btn.color_idle = GREEN
            btn.color_hover = (0, 200, 0)

        # tempo pra animação
        self.time = 0

    def handle_events(self, events):
        for event in events:
            if self.btn_main.is_clicked(event):
                self.manager.set_scene(MainModesScene(self.manager))

            if self.btn_custom.is_clicked(event):
                self.manager.set_scene(CustomModesScene(self.manager))

    def update(self):
        self.time += 0.05  # velocidade da animação

    def get_neon_color(self):
        # ciclo RGB usando seno (efeito neon suave)
        r = int((math.sin(self.time) + 1) * 127)
        g = int((math.sin(self.time + 2) + 1) * 127)
        b = int((math.sin(self.time + 4) + 1) * 127)
        return (r, g, b)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # --- CONTAINER DO TÍTULO ---
        pygame.draw.rect(screen, (0, 0, 0), self.title_box, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.title_box, 2, border_radius=12)

        neon_color = self.get_neon_color()

        # glow (camadas)
        for i in range(3):
            glow_surf = self.font.render("Neon Rush", True, neon_color)
            glow_rect = glow_surf.get_rect(center=self.title_box.center)

            glow_surf.set_alpha(60 - i * 15)
            screen.blit(glow_surf, glow_rect)

        # texto base
        title_surf = self.font.render("Neon Rush", True, neon_color)

        # efeito de escala (cresce e diminui)
        scale = 1 + 0.05 * math.sin(self.time * 2)

        new_width = int(title_surf.get_width() * scale)
        new_height = int(title_surf.get_height() * scale)

        title_surf = pygame.transform.scale(title_surf, (new_width, new_height))

        # centralizar DEPOIS do scale
        title_rect = title_surf.get_rect(center=self.title_box.center)

        screen.blit(title_surf, title_rect)

        # --- CONTAINER DOS BOTÕES ---
        pygame.draw.rect(screen, (30, 30, 30), self.menu_box, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.menu_box, 2, border_radius=12)

        # botões
        self.btn_main.draw(screen)
        self.btn_custom.draw(screen)

        # borda branca dos botões
        pygame.draw.rect(screen, WHITE, self.btn_main.rect, 2, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.btn_custom.rect, 2, border_radius=10)