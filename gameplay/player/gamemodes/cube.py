import pygame
from settings import *
from .base import BaseMode

class CubeMode(BaseMode):
    def __init__(self, player):
        self.player = player

        self.mini = False
        self.gravity = GRAVITY
        self.size = TILE_SIZE

        self.velocity_y = 0

        # Carregamento da imagem
        self.image = pygame.image.load(
            ASSETS_DIR / "objects/player/cube/cube_1.png"
        ).convert_alpha()

        self.scaled_image = self.image

        self.hitbox = pygame.Rect(0, 0, 0, 0)
        self.danger_hitbox = pygame.Rect(0, 0, 0, 0)

    # --- PROPRIEDADES DE GRID (O que adicionamos antes) ---
    @property
    def grid_x(self):
        return self.player.x / TILE_SIZE

    @property
    def grid_y(self):
        return self.player.y / TILE_SIZE

    def set_grid_pos(self, gx, gy):
        self.player.x = gx * TILE_SIZE
        self.player.y = gy * TILE_SIZE

    # --- MÉTODOS DE ATUALIZAÇÃO ---
    def update_size(self):
        """Este é o método que tinha sumido!"""
        if self.mini:
            self.size = int(TILE_SIZE * 0.6)
        else:
            self.size = TILE_SIZE

        self.scaled_image = pygame.transform.scale(
            self.image, (self.size, self.size)
        )

    def update(self, solids):
        # 1. Atualiza o tamanho e imagem
        self.update_size()

        # 2. Física
        # Movimento Horizontal Constante (Estilo GD)
        self.player.x += SPEED

        # Gravidade e Movimento Vertical
        self.velocity_y += self.gravity
        self.player.y += self.velocity_y

        # 3. Atualiza Hitboxes
        self.hitbox = pygame.Rect(self.player.x, self.player.y, self.size, self.size)
        
        shrink = int(self.size * 0.15)
        self.danger_hitbox = pygame.Rect(
            self.player.x + shrink,
            self.player.y + shrink,
            self.size - shrink * 2,
            self.size - shrink * 2
        )

        # 4. Colisão com o chão
        for obj in solids:
            if self.hitbox.colliderect(obj.rect):
                # Colisão de cima para baixo (Chão)
                if self.velocity_y > 0:
                    self.player.y = obj.rect.top - self.size
                    self.velocity_y = 0
                
                # BÔNUS: Colisão de frente (Parede)
                # Se o player bater de frente em um bloco, ele deve morrer
                elif self.hitbox.right > obj.rect.left and self.hitbox.left < obj.rect.left:
                    print("Game Over! Bateu na parede.")
                    # Aqui você chamaria sua função de reset

    def draw(self, screen, camera_x):
        screen.blit(
            self.scaled_image,
            (self.player.x - camera_x, self.player.y)
        )