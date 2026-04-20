import pygame
from settings import IMAGES, TILE_SIZE


def rotate_surface(image, rotation):
    if rotation % 360 == 0:
        return image
    return pygame.transform.rotate(image, rotation)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation=0):
        super().__init__()
        self.base_image = IMAGES["block"]
        self.rotation = rotation % 360
        self.image = rotate_surface(self.base_image, self.rotation)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.blue_hitbox = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE).inflate(-2, -2)


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation=0):
        super().__init__()
        self.base_image = IMAGES["spike"]
        self.rotation = rotation % 360
        self.image = rotate_surface(self.base_image, self.rotation)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.red_hitbox = self._build_hitbox(x, y)

    def _build_hitbox(self, x, y):
        if self.rotation == 0:
            return pygame.Rect(x + 9, y + 8, 22, 28)
        if self.rotation == 180:
            return pygame.Rect(x + 9, y + 4, 22, 28)
        if self.rotation == 90:
            return pygame.Rect(x + 4, y + 9, 28, 22)
        return pygame.Rect(x + 8, y + 9, 28, 22)


class Saw(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation=0):
        super().__init__()
        self.orig = IMAGES["saw"]
        self.image = self.orig.copy()
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        self.angle = rotation % 360
        self.center = pygame.Vector2(self.rect.center)
        self.red_hitbox = pygame.Rect(0, 0, 28, 28)
        self.red_hitbox.center = self.rect.center

    def update(self):
        self.angle += 8
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect(center=(round(self.center.x), round(self.center.y)))
        self.red_hitbox.center = self.rect.center


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, p_type, rotation=0):
        super().__init__()
        self.type = p_type
        self.rotation = rotation % 360
        mapping = {"s": "p_ship", "w": "p_wave", "c": "p_cube", "gi": "p_grav", "gn": "p_grav"}
        base_image = IMAGES.get(mapping.get(p_type, "p_ship"), IMAGES["p_ship"])
        self.image = rotate_surface(base_image, self.rotation)
        self.rect = self.image.get_rect(topleft=(x, y))
        w = TILE_SIZE if self.rotation in (90, 270) else max(10, self.rect.width - 12)
        h = max(20, self.rect.height - 20) if self.rotation in (0, 180) else TILE_SIZE
        self.portal_hitbox = pygame.Rect(x + 6, y + 10, w, h)


class Slope(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation=0):
        super().__init__()
        self.base_image = IMAGES["slope"]
        self.rotation = rotation % 360
        self.image = rotate_surface(self.base_image, self.rotation)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.blue_hitbox = pygame.Rect(x + 2, y + 8, 36, 30)


class Orb(pygame.sprite.Sprite):
    def __init__(self, x, y, orb_type="y"):
        super().__init__()
        self.type = orb_type
        self.image = IMAGES.get("orb_y", pygame.Surface((30, 30)))
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))


class Pad(pygame.sprite.Sprite):
    def __init__(self, x, y, pad_type="y"):
        super().__init__()
        self.type = pad_type
        self.image = IMAGES.get("pad_y", pygame.Surface((40, 15)))
        self.rect = self.image.get_rect(midbottom=(x + TILE_SIZE // 2, y + TILE_SIZE))
