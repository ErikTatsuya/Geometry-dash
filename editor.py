import pygame
import pyperclip
from settings import *

class Editor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Geometry Dash Level Editor")
        self.clock = pygame.time.Clock()
        
        self.camera_x = 0
        self.objects = {} # {(x, y): "id,tipo"}
        
        # Sistema de Abas
        self.tabs = ["BLOCKS", "SPIKES", "SAWS", "PORTALS", "ORBS/PADS"]
        self.current_tab = 0
        
        # Mapeamento de itens por aba: (ID, Nome, Imagem_Key, Subtipo)
        self.items = {
            0: [("1", "Block", "block", None), ("5", "Slope", "slope", None)],
            1: [("2", "Spike", "spike", None)],
            2: [("3", "Saw", "saw", None)],
            3: [("4", "Ship P.", "p_ship", "s"), ("4", "Wave P.", "p_wave", "w"), 
                ("4", "Cube P.", "p_cube", "c"), ("4", "Grav P.", "p_grav", "gi")],
            4: [("6", "Yellow Orb", "orb_y", "y"), ("7", "Yellow Pad", "pad_y", "y")] 
        }
        
        self.selected_item_idx = 0
        self.ui_height = 150 # Altura do painel inferior

    def get_grid_pos(self, pos):
        x = ((pos[0] + self.camera_x) // TILE_SIZE) * TILE_SIZE
        y = (pos[1] // TILE_SIZE) * TILE_SIZE
        return x, y

    def draw_ui(self):
        # Fundo do Painel
        pygame.draw.rect(self.screen, (20, 20, 20), (0, HEIGHT - self.ui_height, WIDTH, self.ui_height))
        pygame.draw.line(self.screen, (100, 100, 100), (0, HEIGHT - self.ui_height), (WIDTH, HEIGHT - self.ui_height), 2)

        # Desenhar Abas
        tab_width = WIDTH // len(self.tabs)
        for i, tab in enumerate(self.tabs):
            color = (50, 50, 50) if i != self.current_tab else (100, 100, 255)
            rect = (i * tab_width, HEIGHT - self.ui_height, tab_width, 30)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
            
            text = FONT_HUD.render(tab, True, (255, 255, 255))
            self.screen.blit(text, (i * tab_width + 10, HEIGHT - self.ui_height + 5))

        # Desenhar Itens da Aba Selecionada
        for i, (obj_id, name, img_key, subtype) in enumerate(self.items[self.current_tab]):
            x = 20 + (i * 70)
            y = HEIGHT - self.ui_height + 50
            rect = (x, y, 60, 60)
            
            # Highlight se selecionado
            bg_color = (80, 80, 80) if i == self.selected_item_idx else (40, 40, 40)
            pygame.draw.rect(self.screen, bg_color, rect)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
            
            # Tenta desenhar o ícone (usa fallback se não houver a imagem ainda)
            try:
                img = pygame.transform.scale(IMAGES[img_key], (40, 40))
                self.screen.blit(img, (x + 10, y + 10))
            except:
                pygame.draw.rect(self.screen, (255,0,0), (x+20, y+20, 20, 20))

    def save_level(self):
        level_str = ""
        for (x, y), val in self.objects.items():
            level_str += f"{val},{x},{y};"
        pyperclip.copy(level_str)
        print("\n--- LEVEL COPIADO ---\n" + level_str)

    def run(self):
        while True:
            self.screen.fill(BG_COLOR)
            mouse_pos = pygame.mouse.get_pos()
            in_ui = mouse_pos[1] > HEIGHT - self.ui_height

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if in_ui:
                        # Clique nas Abas
                        if mouse_pos[1] < HEIGHT - self.ui_height + 30:
                            self.current_tab = mouse_pos[0] // (WIDTH // len(self.tabs))
                            self.selected_item_idx = 0
                        # Clique nos Itens
                        else:
                            idx = (mouse_pos[0] - 20) // 70
                            if 0 <= idx < len(self.items[self.current_tab]):
                                self.selected_item_idx = idx
                    else:
                        grid_pos = self.get_grid_pos(mouse_pos)
                        if event.button == 1: # Esquerdo: Coloca
                            item = self.items[self.current_tab][self.selected_item_idx]
                            # Formato: ID,0,SUBTYPE (O 0 é placeholder pro X que será preenchido no save)
                            val = f"{item[0]},0,{item[3]}" if item[3] else f"{item[0]}"
                            self.objects[grid_pos] = val
                        elif event.button == 3: # Direito: Remove
                            if grid_pos in self.objects: del self.objects[grid_pos]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s: self.save_level()

            # Câmera
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]: self.camera_x += 10
            if keys[pygame.K_LEFT]: self.camera_x = max(0, self.camera_x - 10)

            # Desenhar Grade e Objetos
            for (x, y), val in self.objects.items():
                parts = val.split(',')
                obj_id = parts[0]
                # Lógica visual para o editor
                img_key = "block"
                if obj_id == "1": img_key = "block"
                elif obj_id == "2": img_key = "spike"
                elif obj_id == "3": img_key = "saw"
                elif obj_id == "5": img_key = "slope"
                elif obj_id == "4":
                    st = parts[2]
                    img_key = {"s":"p_ship", "w":"p_wave", "c":"p_cube", "gi":"p_grav"}.get(st, "p_ship")
                
                self.screen.blit(IMAGES.get(img_key, IMAGES['block']), (x - self.camera_x, y))

            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Editor().run()