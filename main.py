import pygame
import sys

# 1. Inicialização imediata do motor de vídeo
pygame.init()

# 2. Definição de constantes básicas para evitar import precoce
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Python")

# 3. Agora que o video mode está definido, importamos o resto
import settings
from level_manager import LevelManager
from entities.player import Player
from entities.objects import Block, Spike, Saw, Portal, Slope

class Game:
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.lm = LevelManager()
        self.state = "MENU"
        self.running = True
        
        self.player = None
        self.camera_x = 0
        self.attempts = 1
        self.last_loaded_data = None
        self.level_width = 0
        
        self.editor_objects = {} 
        self.editor_camera_x = 0
        self.current_tab = 0
        self.level_name = "novo_nivel"
        self.reset_groups()

    def reset_groups(self):
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

    def start_level(self, level_data):
        self.reset_groups()
        self.last_loaded_data = level_data
        self.player = Player()
        self.all_sprites.add(self.player)
        self.camera_x = 0
        
        max_x = 800
        for obj in level_data["objects"]:
            x, y, id_obj = obj["x"], obj["y"], obj["id"]
            if x > max_x: max_x = x
            if id_obj == "1": item = Block(x, y); self.blocks.add(item)
            elif id_obj == "2": item = Spike(x, y); self.hazards.add(item)
            elif id_obj == "3": item = Saw(x, y); self.hazards.add(item)
            elif id_obj == "4": item = Portal(x, y, obj.get("type", "s")); self.portals.add(item)
            elif id_obj == "5": item = Slope(x, y); self.blocks.add(item)
            self.all_sprites.add(item)
            
        self.level_width = max_x + 1000
        self.state = "PLAYING"

    def menu_scene(self):
        self.screen.fill(settings.BG_COLOR)
        # Acessando via settings.IMAGES para garantir que o objeto global seja lido
        if 'bg' in settings.IMAGES:
            self.screen.blit(settings.IMAGES['bg'], (0,0))
        
        title_surf = settings.FONT_TITLE.render("GEOMETRY DASH", True, settings.WHITE)
        self.screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 120))
        
        btn_play = pygame.Rect(WIDTH//2 - 110, 280, 220, 70)
        btn_edit = pygame.Rect(WIDTH//2 - 110, 370, 220, 70)
        
        pygame.draw.rect(self.screen, settings.GREEN_BUTTON, btn_play, border_radius=15)
        pygame.draw.rect(self.screen, settings.UI_ACCENT, btn_edit, border_radius=15)
        
        txt_p = settings.FONT_HUD.render("JOGAR", True, settings.WHITE)
        txt_e = settings.FONT_HUD.render("EDITOR", True, settings.WHITE)
        self.screen.blit(txt_p, (btn_play.centerx - txt_p.get_width()//2, btn_play.centery - txt_p.get_height()//2))
        self.screen.blit(txt_e, (btn_edit.centerx - txt_e.get_width()//2, btn_edit.centery - txt_e.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.collidepoint(event.pos): self.state = "SELECT"
                if btn_edit.collidepoint(event.pos): self.state = "EDITOR_MENU"

    def select_scene(self):
        self.screen.fill(settings.BG_COLOR)
        pygame.draw.rect(self.screen, settings.UI_BG, (30, 30, WIDTH-60, HEIGHT-60), border_radius=20)
        header = settings.FONT_TITLE.render("SELECIONE O NÍVEL", True, settings.UI_ACCENT)
        self.screen.blit(header, (WIDTH//2 - header.get_width()//2, 50))
        
        levels = self.lm.list_files("main") + self.lm.list_files("custom")
        for i, name in enumerate(levels[:6]):
            card = pygame.Rect(60, 135 + i*65, WIDTH-120, 55)
            pygame.draw.rect(self.screen, (45, 50, 80), card, border_radius=10)
            self.screen.blit(settings.FONT_HUD.render(name.upper(), True, settings.WHITE), (90, 150 + i*65))
            
            if pygame.mouse.get_pressed()[0] and card.collidepoint(pygame.mouse.get_pos()):
                folder = "main" if name in self.lm.list_files("main") else "custom"
                data = self.lm.load(name, folder)
                self.attempts = 1
                self.start_level(data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.state = "MENU"

    def editor_menu_scene(self):
        self.screen.fill(settings.BG_COLOR)
        pygame.draw.rect(self.screen, settings.UI_BG, (100, 100, WIDTH-200, HEIGHT-200), border_radius=20)
        btn_novo = pygame.Rect(WIDTH//2-120, 220, 240, 60)
        btn_exit = pygame.Rect(WIDTH//2-120, 300, 240, 60)
        pygame.draw.rect(self.screen, (60, 70, 120), btn_novo, border_radius=10)
        pygame.draw.rect(self.screen, (120, 60, 60), btn_exit, border_radius=10)
        self.screen.blit(settings.FONT_HUD.render("CRIAR NOVO", True, settings.WHITE), (btn_novo.centerx-50, btn_novo.centery-10))
        self.screen.blit(settings.FONT_HUD.render("VOLTAR", True, settings.WHITE), (btn_exit.centerx-30, btn_exit.centery-10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_novo.collidepoint(event.pos): self.state = "EDITOR_REAL"
                if btn_exit.collidepoint(event.pos): self.state = "MENU"

    def editor_real_scene(self):
        self.screen.fill(settings.BG_COLOR)
        ui_h = 160
        grid_area = HEIGHT - ui_h
        
        for x in range(0, WIDTH + settings.TILE_SIZE, settings.TILE_SIZE):
            lx = x - (self.editor_camera_x % settings.TILE_SIZE)
            pygame.draw.line(self.screen, (30, 35, 60), (lx, 0), (lx, grid_area))
        
        for (ox, oy), obj_id in self.editor_objects.items():
            dx = ox - self.editor_camera_x
            if -settings.TILE_SIZE < dx < WIDTH:
                img_key = {"1":'block',"2":'spike',"3":'saw',"5":'slope'}.get(obj_id, 'block')
                self.screen.blit(settings.IMAGES[img_key], (dx, oy))

        pygame.draw.rect(self.screen, settings.UI_BG, (0, grid_area, WIDTH, ui_h))
        tabs = ["BLOCKS", "SPIKES", "SAWS", "PORTALS"]
        tw = WIDTH // len(tabs)
        for i, t in enumerate(tabs):
            c = settings.UI_ACCENT if self.current_tab == i else (50, 60, 100)
            pygame.draw.rect(self.screen, c, (i*tw, grid_area, tw, 35))
            self.screen.blit(settings.FONT_HUD.render(t, True, settings.WHITE), (i*tw + 20, grid_area + 8))

        btn_s = pygame.Rect(WIDTH-115, 15, 100, 35)
        btn_t = pygame.Rect(WIDTH-115, 60, 100, 35)
        pygame.draw.rect(self.screen, settings.GREEN_BUTTON, btn_s, border_radius=8)
        pygame.draw.rect(self.screen, settings.UI_ACCENT, btn_t, border_radius=8)
        self.screen.blit(settings.FONT_HUD.render("SALVAR", True, settings.WHITE), (btn_s.x+15, btn_s.y+7))
        self.screen.blit(settings.FONT_HUD.render("TESTAR", True, settings.WHITE), (btn_t.x+15, btn_t.y+7))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if my < grid_area:
                    gx = ((mx + self.editor_camera_x) // settings.TILE_SIZE) * settings.TILE_SIZE
                    gy = (my // settings.TILE_SIZE) * settings.TILE_SIZE
                    if event.button == 1: self.editor_objects[(gx, gy)] = str(self.current_tab + 1)
                    if event.button == 3: self.editor_objects.pop((gx, gy), None)
                elif grid_area < my < grid_area + 35:
                    self.current_tab = mx // tw
                elif btn_s.collidepoint(mx, my):
                    self.lm.save(self.level_name, self.editor_objects, {"name": self.level_name})
                elif btn_t.collidepoint(mx, my):
                    self.start_level({"objects": [{"id":v,"x":k[0],"y":k[1]} for k,v in self.editor_objects.items()]})
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: self.editor_camera_x += settings.TILE_SIZE * 2
                if event.key == pygame.K_LEFT: self.editor_camera_x = max(0, self.editor_camera_x - settings.TILE_SIZE * 2)
                if event.key == pygame.K_ESCAPE: self.state = "EDITOR_MENU"

    def play_scene(self):
        self.screen.fill(settings.BG_COLOR)
        self.screen.blit(settings.IMAGES['bg'], (0,0))
        self.camera_x += 6
        self.player.rect.x = self.camera_x + 100
        self.all_sprites.update()

        hits = pygame.sprite.spritecollide(self.player, self.blocks, False)
        for b in hits:
            if self.player.gravity_dir == 1 and self.player.vel_y > 0:
                self.player.rect.bottom = b.rect.top
                self.player.vel_y = 0; self.player.on_ground = True

        if pygame.sprite.spritecollide(self.player, self.hazards, False) or self.player.rect.y > HEIGHT:
            self.attempts += 1
            self.start_level(self.last_loaded_data)

        for s in self.all_sprites:
            self.screen.blit(s.image, (s.rect.x - self.camera_x, s.rect.y))
        
        prog = min(100, int((self.camera_x / (self.level_width - WIDTH)) * 100))
        pygame.draw.rect(self.screen, (50, 50, 50), (WIDTH//2-100, 30, 200, 12), border_radius=6)
        pygame.draw.rect(self.screen, settings.UI_ACCENT, (WIDTH//2-100, 30, prog*2, 12), border_radius=6)
        self.screen.blit(settings.FONT_HUD.render(f"ATTEMPT {self.attempts}", True, settings.WHITE), (20, 20))
        self.screen.blit(settings.FONT_HUD.render(f"{prog}%", True, settings.WHITE), (WIDTH//2+110, 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.state = "SELECT"

    def run(self):
        while self.running:
            if self.state == "MENU": self.menu_scene()
            elif self.state == "SELECT": self.select_scene()
            elif self.state == "PLAYING": self.play_scene()
            elif self.state == "EDITOR_MENU": self.editor_menu_scene()
            elif self.state == "EDITOR_REAL": self.editor_real_scene()
            pygame.display.flip()
            self.clock.tick(settings.FPS)
        pygame.quit()

if __name__ == "__main__":
    Game().run()