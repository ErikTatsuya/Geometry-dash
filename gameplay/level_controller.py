import pygame
from gameplay.player.player import Player
from settings import *

class LevelController:
    def __init__(self, level):
        self.level = level
        self.camera_x = 0
        self.bg_image = None

        # Carregamento do Background
        bg_path = self.level.metadata.get("background")
        if bg_path:
            full_path = ASSETS_DIR / bg_path
            self.bg_image = pygame.image.load(str(full_path)).convert()

        # Passa a tupla START_POS diretamente (ex: (10, 5))
        # Certifique-se que o __init__ do seu Player trate x = pos[0] e y = pos[1]
        self.player = Player(START_POS)

    def update(self):
        solids = self.level.get_solids()
        self.player.update(solids)

        # Cálculo da Câmera Suave (Lerp)
        # target_x é onde o player está menos o recuo da tela (200px)
        target_x = self.player.x - 200
        
        # Suavização: a câmera se move 10% da distância restante a cada frame
        self.camera_x += (target_x - self.camera_x) * 0.1

        # Trava para a câmera não mostrar o "vazio" antes do X=0
        if self.camera_x < 0:
            self.camera_x = 0

        self.level.update()

    def draw(self, screen):
        screen.fill(BLACK)

        # Desenha o fundo com Parallax (0.3 faz o fundo parecer mais distante)
        if self.bg_image:
            screen.blit(self.bg_image, (-self.camera_x * 0.3, 0))

        # Desenha os blocos/espinhos do nível
        for obj in self.level.objects:
            obj.draw(screen, self.camera_x)

        # Desenha o player
        self.player.draw(screen, self.camera_x)