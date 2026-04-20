import pygame
from settings import *
from entities.player import Player
from entities.objects import Block, Spike, Saw, Portal
from level_data import LEVEL_01

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Geometry Dash 3.14")
        self.clock = pygame.time.Clock()
        self.camera_x = 0
        self.attempts = 1  # Contador de tentativas inicial
        self.level_width = 0 # Será calculado no load_level
        self.reset()

    def reset(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.blocks = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.load_level(LEVEL_01)
        self.camera_x = 0

    def load_level(self, data):
        max_x = 0
        for item in data.split(';')[:-1]:
            parts = item.split(',')
            obj_id, x, y = parts[0], int(parts[1]), int(parts[2])
            
            # Descobrir o final do nível para a porcentagem
            if x > max_x: max_x = x
            
            if obj_id == "1":
                obj = Block(x, y); self.blocks.add(obj)
            elif obj_id == "2":
                obj = Spike(x, y); self.hazards.add(obj)
            elif obj_id == "3":
                obj = Saw(x, y); self.hazards.add(obj)
            elif obj_id == "4":
                obj = Portal(x, y, parts[3]); self.portals.add(obj)
            
            self.all_sprites.add(obj)
        
        self.level_width = max_x + 400 # Margem após o último objeto

    def draw_hud(self):
        # 1. Cálculo da Porcentagem
        # Progresso vai de 0 até o level_width
        progress = min(100, int((self.camera_x / (self.level_width - WIDTH)) * 100))
        if progress < 0: progress = 0

        # 2. Desenhar Barra de Porcentagem (Topo da tela)
        bar_w, bar_h = 200, 15
        bar_x, bar_y = (WIDTH // 2) - (bar_w // 2), 20
        
        # Fundo da barra
        pygame.draw.rect(self.screen, BAR_COLOR_BG, (bar_x, bar_y, bar_w, bar_h))
        # Preenchimento
        pygame.draw.rect(self.screen, BAR_COLOR_FILL, (bar_x, bar_y, int(bar_w * (progress/100)), bar_h))
        
        # Texto da Porcentagem
        perc_text = FONT_HUD.render(f"{progress}%", True, (255, 255, 255))
        self.screen.blit(perc_text, (bar_x + bar_w + 10, bar_y - 5))

        # 3. Desenhar Contador de Attempts (Canto superior esquerdo)
        att_text = FONT_HUD.render(f"Attempt {self.attempts}", True, (255, 255, 255))
        self.screen.blit(att_text, (20, 20))

    def run(self):
        running = True
        while running:
            self.screen.fill(BG_COLOR)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Progressão
            self.camera_x += 5
            self.player.rect.x = self.camera_x + 100
            self.all_sprites.update()

            # Colisões com Blocos
            hits = pygame.sprite.spritecollide(self.player, self.blocks, False)
            for block in hits:
                if self.player.gravity_dir == 1 and self.player.vel_y > 0:
                    self.player.rect.bottom = block.rect.top
                    self.player.vel_y = 0
                    self.player.on_ground = True
                elif self.player.gravity_dir == -1 and self.player.vel_y < 0:
                    self.player.rect.top = block.rect.bottom
                    self.player.vel_y = 0
                    self.player.on_ground = True

            # Colisões de Morte
            if pygame.sprite.spritecollide(self.player, self.hazards, False) or \
               self.player.rect.bottom > HEIGHT + 200 or self.player.rect.top < -200:
                self.attempts += 1 # Aumenta tentativa ao morrer
                self.reset()

            # Portais
            p_hits = pygame.sprite.spritecollide(self.player, self.portals, False)
            for p in p_hits:
                if p.type == "s": self.player.mode = "ship"
                elif p.type == "w": self.player.mode = "wave"
                elif p.type == "c": self.player.mode = "cube"
                elif p.type == "gi": self.player.gravity_dir = -1
                elif p.type == "gn": self.player.gravity_dir = 1

            # Desenho dos Sprites
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))

            # Desenho do HUD (Barra e Attempts)
            self.draw_hud()

            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    Game().run()