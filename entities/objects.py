import pygame
from settings import IMAGES, TILE_SIZE

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = IMAGES['block']
        self.rect = self.image.get_rect(topleft=(x, y))

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = IMAGES['spike']
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

class Saw(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.orig = IMAGES['saw']
        self.image = self.orig.copy()
        self.rect = self.image.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
        self.angle = 0
    def update(self):
        self.angle += 8
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, p_type):
        super().__init__()
        self.type = p_type
        mapping = {"s": 'p_ship', "w": 'p_wave', "c": 'p_cube', "gi": 'p_grav', "gn": 'p_grav'}
        self.image = IMAGES.get(mapping.get(p_type, 'p_ship'), IMAGES['p_ship'])
        self.rect = self.image.get_rect(topleft=(x, y))

class Slope(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = IMAGES['slope']
        self.rect = self.image.get_rect(topleft=(x, y))
        # Máscara para colisão precisa em rampa
        self.mask = pygame.mask.from_surface(self.image)

# Adicionando Orbs e Pads para evitar erros futuros
class Orb(pygame.sprite.Sprite):
    def __init__(self, x, y, orb_type="y"):
        super().__init__()
        self.type = orb_type
        self.image = IMAGES.get('orb_y', pygame.Surface((30,30)))
        self.rect = self.image.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))

class Pad(pygame.sprite.Sprite):
    def __init__(self, x, y, pad_type="y"):
        super().__init__()
        self.type = pad_type
        self.image = IMAGES.get('pad_y', pygame.Surface((40,15)))
        self.rect = self.image.get_rect(midbottom=(x + TILE_SIZE//2, y + TILE_SIZE))