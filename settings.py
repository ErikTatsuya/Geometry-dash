import pygame
import os

# --- Configurações de Tela e Física ---
WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40
GRAVITY = 0.35

# --- Cores de Fallback (usadas se as imagens não forem encontradas) ---
BG_COLOR = (10, 10, 30)
BLUE = (0, 200, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 100)
BAR_COLOR_BG = (50, 50, 50)
BAR_COLOR_FILL = (0, 255, 100)

def get_image(path, size, color=(255, 255, 255)):
    """
    Carrega uma imagem da pasta 'assets'. 
    Se falhar, cria uma superfície colorida de reserva.
    """
    full_path = os.path.join('assets', path)
    try:
        img = pygame.image.load(full_path).convert_alpha()
        return pygame.transform.scale(img, size)
    except Exception as e:
        # Se a imagem não existir, cria um bloco colorido para o jogo não travar
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        # Se for um espinho, desenha um triângulo no fallback
        if 'spike' in path:
            pygame.draw.polygon(surf, color, [(size[0]//2, 0), (0, size[1]), (size[0], size[1])])
        return surf

# --- Inicialização para carregar Assets ---
pygame.display.init()
pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
FONT_HUD = pygame.font.SysFont("Arial", 22, bold=True)

# --- Dicionário de Imagens (Mapeado para seus arquivos reais) ---
IMAGES = {
    # Personagens e Modos
    'cube':   get_image('cube.png', (38, 38), BLUE),
    'ship':   get_image('ship.png', (45, 25), GREEN),
    'wave':   get_image('wave.png', (30, 30), YELLOW),
    
    # Obstáculos (Nomes ajustados para seu dir)
    'spike':  get_image('spike.png', (40, 40), (255, 50, 50)),
    'block':  get_image('block_solid.png', (40, 40), (150, 150, 150)),
    'saw':    get_image('saw_blade.png', (50, 50), (255, 255, 255)),
    'slope':  get_image('slope.png', (40, 40), (100, 100, 100)),
    
    # Cenário
    'bg':     get_image('bg_main.png', (WIDTH, HEIGHT), BG_COLOR),
    
    # Portais (Mapeado para seus arquivos reais)
    'p_ship': get_image('portal_ship.png', (45, 110), (0, 255, 0)),
    'p_wave': get_image('portal_wave.png', (45, 110), (0, 200, 255)),
    'p_cube': get_image('portal_cube.png', (45, 110), (0, 100, 255)),
    'p_grav': get_image('portal_gravity.png', (45, 110), (255, 255, 0))
}