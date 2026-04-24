import pygame
import os
from pathlib import Path

# --- Configuração de Caminhos ---
BASE_DIR = Path(__file__).parent.absolute()
ASSETS_DIR = BASE_DIR / "assets"

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 50
GRAVITY = 0.35

BG_COLOR = (10, 15, 35)       
UI_BG = (25, 30, 100)          
UI_ACCENT = (0, 200, 255)     
GREEN_BUTTON = (40, 210, 100) 
WHITE = (240, 240, 240)

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
FONT_HUD = pygame.font.SysFont("Arial", 20, bold=True)
FONT_TITLE = pygame.font.SysFont("Arial", TILE_SIZE, bold=True)

# Chaves padronizadas para o main.py
IMAGES = {
    'cube':   get_image('cube.png', (TILE_SIZE, TILE_SIZE), (0, 200, 255)),
    'ship':   get_image('ship.png', (TILE_SIZE, TILE_SIZE * 0.5), (0, 255, 100)),
    'wave':   get_image('wave.png', (TILE_SIZE * 0.5, TILE_SIZE), (255, 255, 0)),
    
    'block':  get_image('block_solid.png', (TILE_SIZE, TILE_SIZE), (100,100,100)),
    'spike':  get_image('spike.png', (TILE_SIZE, TILE_SIZE), (255, 50, 50)),
    'saw':    get_image('saw_blade.png', (TILE_SIZE, TILE_SIZE), (200, 200, 200)),
    'slope':  get_image('slope.png', (TILE_SIZE, TILE_SIZE), (80, 80, 80)),
    
    'bg':     get_image('bg_main.png', (WIDTH, HEIGHT), BG_COLOR), # Chave 'bg' restaurada
    
    'p_ship': get_image('portal_ship.png', (TILE_SIZE, TILE_SIZE * 2), (0, 255, 0)),
    'p_wave': get_image('portal_wave.png', (TILE_SIZE, TILE_SIZE * 2), (0, 200, 255)),
    'p_cube': get_image('portal_cube.png', (TILE_SIZE, TILE_SIZE * 2), (0, TILE_SIZE * 2, 255)),
    'p_grav_up': get_image('portal_gravity_up.png', (TILE_SIZE, TILE_SIZE * 2), (200, 0, 255)),
    'p_grav_down': get_image('portal_gravity_down.png', (TILE_SIZE, TILE_SIZE * 2), (200, 0, 255))
}