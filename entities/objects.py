import pygame
from settings import IMAGES

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Usa a imagem block_solid.png redimensionada no settings
        self.image = IMAGES['block']
        self.rect = self.image.get_rect(topleft=(x, y))

class Slope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Usa a imagem slope.png
        self.image = IMAGES['slope']
        self.rect = self.image.get_rect(topleft=(x, y))
        # Máscara para colisões precisas em rampas (opcional para o motor atual)
        self.mask = pygame.mask.from_surface(self.image)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Usa a imagem spike.png
        self.image = IMAGES['spike']
        self.rect = self.image.get_rect(topleft=(x, y))
        # Define a máscara para evitar mortes injustas por encostar no vazio do PNG
        self.mask = pygame.mask.from_surface(self.image)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, p_type):
        super().__init__()
        self.type = p_type  # s, w, c, gi, gn
        
        # Mapeamento para garantir que cada tipo use seu respectivo asset
        portal_map = {
            "s":  IMAGES['p_ship'],
            "w":  IMAGES['p_wave'],
            "c":  IMAGES['p_cube'],
            "gi": IMAGES['p_grav'],  # Gravidade Inversa
            "gn": IMAGES['p_grav']   # Gravidade Normal
        }
        
        # Seleciona a imagem baseada no tipo; se não achar, usa ship como padrão
        self.image = portal_map.get(p_type, IMAGES['p_ship'])
        self.rect = self.image.get_rect(topleft=(x, y))

class Saw(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Salva a imagem original para evitar distorção ao rotacionar
        self.original_image = IMAGES['saw']
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0

    def update(self):
        # Faz a serra girar constantemente
        self.angle += 10
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Recalcula o rect mantendo o centro para o giro não "sambalear"
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)