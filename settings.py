import pygame
import os
from pathlib import Path

# --- Configuração de Caminhos ---
BASE_DIR = Path(__file__).parent.absolute()

ASSETS_DIR = BASE_DIR / "assets"
LEVELS_PATH = BASE_DIR / "levels"
MAIN_LEVELS = LEVELS_PATH / "main"
CUSTOM_LEVELS = LEVELS_PATH / "custom"

WIDTH, HEIGHT = 800, 600
MIDDLE_X, MIDDLE_Y = WIDTH / 2, HEIGHT / 2
FPS = 60
TILE_SIZE = 40
GRAVITY = 0.35


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (64, 255, 64)

def get_image(filename, size, color):
    full_path = ASSETS_DIR / filename
    if full_path.exists():
        try:
            # O display já estará pronto por causa da ordem no main.py
            img = pygame.image.load(str(full_path)).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")
    
    surf = pygame.Surface(size)
    surf.fill(color)
    pygame.draw.rect(surf, WHITE, surf.get_rect(), 1)
    return surf

pygame.font.init()
