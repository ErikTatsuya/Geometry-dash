import math
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Python")

import settings
from level_manager import LevelManager
from entities.player import Player
from entities.objects import Block, Spike, Saw, Portal, Slope
from systems.editor import EDITOR_TABS, EDIT_TOOLS, EditorState, draw_text_input, infer_image_key, make_object_data
from systems.gameplay import (
    apply_portals,
    draw_particles,
    resolve_solid_collisions,
    spawn_death_burst,
    spawn_trail,
    touches_hazard,
    update_particles,
)


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
        self.play_return_state = "SELECT"
        self.particles = []

        self.editor = EditorState()

        self.reset_groups()

    def reset_groups(self):
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

    def reset_editor(self, level_name="novo_nivel", folder="custom", metadata=None):
        self.editor.reset(level_name, folder, metadata)

    def load_level_into_editor(self, name, folder):
        data = self.lm.load(name, folder)
        if not data:
            return

        self.editor.load_level_data(name, folder, data)
        self.state = "EDITOR_SETUP"

    def export_editor_level_data(self):
        return self.editor.export_level_data()

    def start_level(self, level_data, return_state="SELECT"):
        self.reset_groups()
        self.last_loaded_data = level_data
        self.play_return_state = return_state
        self.player = Player()
        self.all_sprites.add(self.player)
        self.camera_x = 0

        max_x = 800
        for obj in level_data["objects"]:
            x, y, id_obj = obj["x"], obj["y"], obj["id"]
            if x > max_x:
                max_x = x
            if id_obj == "1":
                item = Block(x, y, obj.get("rotation", 0))
                self.blocks.add(item)
            elif id_obj == "2":
                item = Spike(x, y, obj.get("rotation", 0))
                self.hazards.add(item)
            elif id_obj == "3":
                item = Saw(x, y, obj.get("rotation", 0))
                self.hazards.add(item)
            elif id_obj == "4":
                item = Portal(x, y, obj.get("type", "s"), obj.get("rotation", 0))
                self.portals.add(item)
            elif id_obj == "5":
                item = Slope(x, y, obj.get("rotation", 0))
                self.blocks.add(item)
            else:
                continue
            self.all_sprites.add(item)

        self.level_width = max_x + 1000
        self.state = "PLAYING"

    def draw_button(self, rect, label, color, hover_color=None):
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)
        pulse = 1 + (0.03 * math.sin(pygame.time.get_ticks() / 140)) if hovered else 1
        scale = 1.06 if hovered else 1.0
        draw_rect = rect.inflate(int(rect.width * (scale - 1) * pulse), int(rect.height * (scale - 1) * pulse))
        shadow_rect = draw_rect.move(0, 5 if hovered else 3)
        current_color = hover_color or tuple(min(255, c + 25) for c in color)

        pygame.draw.rect(self.screen, (10, 12, 22), shadow_rect, border_radius=15)
        pygame.draw.rect(self.screen, current_color if hovered else color, draw_rect, border_radius=15)

        txt = settings.FONT_HUD.render(label, True, settings.WHITE)
        self.screen.blit(txt, (draw_rect.centerx - txt.get_width() // 2, draw_rect.centery - txt.get_height() // 2))
        return hovered

    def draw_text_input(self, rect, label, field_name):
        draw_text_input(self.screen, settings.FONT_HUD, settings.UI_ACCENT, settings.WHITE, rect, label, field_name, self.editor)

    def spawn_trail(self):
        spawn_trail(self)

    def spawn_death_burst(self):
        spawn_death_burst(self)

    def update_particles(self):
        update_particles(self)

    def draw_particles(self):
        draw_particles(self)

    def resolve_solid_collisions(self):
        resolve_solid_collisions(self)

    def touches_hazard(self):
        return touches_hazard(self)

    def draw_player_hitboxes(self):
        blue = self.player.get_blue_hitbox().move(-self.camera_x, 0)
        red = self.player.get_red_hitbox().move(-self.camera_x, 0)
        pygame.draw.rect(self.screen, (50, 180, 255), blue, width=1, border_radius=4)
        pygame.draw.rect(self.screen, (255, 80, 90), red, width=1, border_radius=4)

    def menu_scene(self):
        self.screen.fill(settings.BG_COLOR)
        if "bg" in settings.IMAGES:
            self.screen.blit(settings.IMAGES["bg"], (0, 0))

        title_surf = settings.FONT_TITLE.render("GEOMETRY DASH", True, settings.WHITE)
        self.screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 120))

        btn_play = pygame.Rect(WIDTH // 2 - 110, 280, 220, 70)
        btn_edit = pygame.Rect(WIDTH // 2 - 110, 370, 220, 70)

        self.draw_button(btn_play, "JOGAR", settings.GREEN_BUTTON)
        self.draw_button(btn_edit, "EDITOR", settings.UI_ACCENT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play.collidepoint(event.pos):
                    self.state = "SELECT"
                if btn_edit.collidepoint(event.pos):
                    self.state = "EDITOR_MENU"

    def select_scene(self):
        self.screen.fill(settings.BG_COLOR)
        pygame.draw.rect(self.screen, settings.UI_BG, (30, 30, WIDTH - 60, HEIGHT - 60), border_radius=20)
        header = settings.FONT_TITLE.render("SELECIONE O NIVEL", True, settings.UI_ACCENT)
        self.screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 50))

        main_levels = self.lm.list_files("main")
        custom_levels = self.lm.list_files("custom")
        levels = [("main", name) for name in main_levels] + [("custom", name) for name in custom_levels]
        for i, (folder, name) in enumerate(levels[:6]):
            card = pygame.Rect(60, 135 + i * 65, WIDTH - 120, 55)
            hovered = card.collidepoint(pygame.mouse.get_pos())
            draw_card = card.inflate(10 if hovered else 0, 6 if hovered else 0)
            pygame.draw.rect(self.screen, (60, 68, 108) if hovered else (45, 50, 80), draw_card, border_radius=12)
            self.screen.blit(settings.FONT_HUD.render(f"{name.upper()} [{folder.upper()}]", True, settings.WHITE), (90, 150 + i * 65))

            if pygame.mouse.get_pressed()[0] and card.collidepoint(pygame.mouse.get_pos()):
                data = self.lm.load(name, folder)
                self.attempts = 1
                self.start_level(data, "SELECT")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "MENU"

    def editor_menu_scene(self):
        self.screen.fill(settings.BG_COLOR)
        pygame.draw.rect(self.screen, settings.UI_BG, (100, 100, WIDTH - 200, HEIGHT - 200), border_radius=20)
        title = settings.FONT_TITLE.render("EDITOR DE NIVEIS", True, settings.UI_ACCENT)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 135))

        btn_novo = pygame.Rect(WIDTH // 2 - 140, 220, 280, 60)
        btn_editar = pygame.Rect(WIDTH // 2 - 140, 300, 280, 60)
        btn_exit = pygame.Rect(WIDTH // 2 - 140, 380, 280, 60)
        self.draw_button(btn_novo, "CRIAR NOVO", (60, 70, 120))
        self.draw_button(btn_editar, "EDITAR EXISTENTE", settings.UI_ACCENT)
        self.draw_button(btn_exit, "VOLTAR", (120, 60, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_novo.collidepoint(event.pos):
                    self.reset_editor()
                    self.state = "EDITOR_SETUP"
                if btn_editar.collidepoint(event.pos):
                    self.state = "EDITOR_SELECT"
                if btn_exit.collidepoint(event.pos):
                    self.state = "MENU"

    def editor_select_scene(self):
        self.screen.fill(settings.BG_COLOR)
        pygame.draw.rect(self.screen, settings.UI_BG, (30, 30, WIDTH - 60, HEIGHT - 60), border_radius=20)
        header = settings.FONT_TITLE.render("ESCOLHA O NIVEL", True, settings.UI_ACCENT)
        self.screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 50))

        main_levels = self.lm.list_files("main")
        custom_levels = self.lm.list_files("custom")
        levels = [("main", name) for name in main_levels] + [("custom", name) for name in custom_levels]

        for i, (folder, name) in enumerate(levels[:6]):
            card = pygame.Rect(60, 135 + i * 65, WIDTH - 120, 55)
            hovered = card.collidepoint(pygame.mouse.get_pos())
            draw_card = card.inflate(10 if hovered else 0, 6 if hovered else 0)
            pygame.draw.rect(self.screen, (60, 68, 108) if hovered else (45, 50, 80), draw_card, border_radius=12)
            label = f"{name.upper()} [{folder.upper()}]"
            self.screen.blit(settings.FONT_HUD.render(label, True, settings.WHITE), (90, 150 + i * 65))

            if pygame.mouse.get_pressed()[0] and card.collidepoint(pygame.mouse.get_pos()):
                self.load_level_into_editor(name, folder)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "EDITOR_MENU"

    def editor_setup_scene(self):
        self.screen.fill(settings.BG_COLOR)
        panel = pygame.Rect(80, 70, WIDTH - 160, HEIGHT - 140)
        pygame.draw.rect(self.screen, settings.UI_BG, panel, border_radius=22)
        title = settings.FONT_TITLE.render("CONFIGURAR NIVEL", True, settings.UI_ACCENT)
        subtitle = settings.FONT_HUD.render("Nome, descricao e musica antes de abrir o editor", True, settings.WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 95))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 145))

        name_rect = pygame.Rect(140, 210, 520, 48)
        desc_rect = pygame.Rect(140, 295, 520, 48)
        music_rect = pygame.Rect(140, 380, 520, 48)
        btn_continue = pygame.Rect(140, 465, 240, 56)
        btn_back = pygame.Rect(420, 465, 240, 56)

        self.draw_text_input(name_rect, "Nome", "name")
        self.draw_text_input(desc_rect, "Descricao", "description")
        self.draw_text_input(music_rect, "Musica (futuro)", "music")
        self.draw_button(btn_continue, "ABRIR EDITOR", settings.GREEN_BUTTON)
        self.draw_button(btn_back, "VOLTAR", (120, 60, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if name_rect.collidepoint(event.pos):
                    self.editor.form_active = "name"
                elif desc_rect.collidepoint(event.pos):
                    self.editor.form_active = "description"
                elif music_rect.collidepoint(event.pos):
                    self.editor.form_active = "music"
                elif btn_continue.collidepoint(event.pos):
                    chosen_name = self.editor.metadata["name"].strip() or "novo_nivel"
                    self.editor.level_name = chosen_name.replace(" ", "_").lower()
                    self.editor.metadata["name"] = chosen_name
                    self.state = "EDITOR_REAL"
                elif btn_back.collidepoint(event.pos):
                    self.state = "EDITOR_SELECT" if self.editor.pending_open else "EDITOR_MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "EDITOR_SELECT" if self.editor.pending_open else "EDITOR_MENU"
                elif event.key == pygame.K_BACKSPACE:
                    active = self.editor.form_active
                    self.editor.metadata[active] = self.editor.metadata[active][:-1]
                elif event.key == pygame.K_TAB:
                    fields = ["name", "description", "music"]
                    idx = fields.index(self.editor.form_active)
                    self.editor.form_active = fields[(idx + 1) % len(fields)]
                elif event.unicode and event.unicode.isprintable():
                    limit = 34 if self.editor.form_active == "name" else 52
                    current = self.editor.metadata[self.editor.form_active]
                    if len(current) < limit:
                        self.editor.metadata[self.editor.form_active] += event.unicode

    def draw_editor_object(self, obj, screen_pos):
        image_key = obj.get("image_key", infer_image_key(obj))
        source = settings.IMAGES[image_key]
        rotation = obj.get("rotation", 0) % 360
        if rotation:
            source = pygame.transform.rotate(source, rotation)
        width = max(12, int(source.get_width() * self.editor.zoom))
        height = max(12, int(source.get_height() * self.editor.zoom))
        surface = pygame.transform.smoothscale(source, (width, height))
        self.screen.blit(surface, screen_pos)
        return surface.get_rect(topleft=screen_pos)

    def editor_world_to_screen(self, x, y):
        return (
            int((x - self.editor.camera_x) * self.editor.zoom),
            int((y - self.editor.camera_y) * self.editor.zoom),
        )

    def get_editor_object_at(self, world_x, world_y):
        for pos, obj in reversed(list(self.editor.objects.items())):
            rect = pygame.Rect(obj["x"], obj["y"], settings.TILE_SIZE, settings.TILE_SIZE)
            if rect.collidepoint(world_x, world_y):
                return pos, obj
        return None, None

    def place_selected_palette_object(self, grid_pos):
        self.editor.push_undo()
        item = self.editor.get_selected_palette_item()
        self.editor.objects[grid_pos] = make_object_data(item, grid_pos)
        self.editor.selected_object_pos = grid_pos

    def delete_editor_object(self, grid_pos):
        if grid_pos not in self.editor.objects:
            return
        self.editor.push_undo()
        self.editor.objects.pop(grid_pos, None)
        if self.editor.selected_object_pos == grid_pos:
            self.editor.selected_object_pos = None

    def move_selected_editor_object(self, dx, dy):
        pos = self.editor.selected_object_pos
        if pos not in self.editor.objects:
            return
        obj = self.editor.objects[pos]
        target = (pos[0] + dx * settings.TILE_SIZE, pos[1] + dy * settings.TILE_SIZE)
        self.editor.push_undo()
        self.editor.objects.pop(pos)
        moved = dict(obj)
        moved["x"], moved["y"] = target
        self.editor.objects[target] = moved
        self.editor.selected_object_pos = target

    def rotate_selected_editor_object(self, delta):
        pos = self.editor.selected_object_pos
        if pos not in self.editor.objects:
            return
        self.editor.push_undo()
        self.editor.objects[pos]["rotation"] = (self.editor.objects[pos].get("rotation", 0) + delta) % 360

    def handle_editor_key_action(self, event):
        if self.editor.mode != "edit":
            return
        if event.key == pygame.K_q:
            self.rotate_selected_editor_object(90)
        elif event.key == pygame.K_e:
            self.rotate_selected_editor_object(-90)
        elif event.key == pygame.K_w:
            self.move_selected_editor_object(0, -1)
        elif event.key == pygame.K_a:
            self.move_selected_editor_object(-1, 0)
        elif event.key == pygame.K_s:
            self.move_selected_editor_object(0, 1)
        elif event.key == pygame.K_d:
            self.move_selected_editor_object(1, 0)

    def editor_real_scene(self):
        self.screen.fill(settings.BG_COLOR)
        ui_h = 220
        grid_area = HEIGHT - ui_h

        visible_world_w = WIDTH / self.editor.zoom
        visible_world_h = grid_area / self.editor.zoom
        start_x = math.floor(self.editor.camera_x / settings.TILE_SIZE) * settings.TILE_SIZE
        end_x = math.ceil((self.editor.camera_x + visible_world_w) / settings.TILE_SIZE) * settings.TILE_SIZE
        start_y = math.floor(self.editor.camera_y / settings.TILE_SIZE) * settings.TILE_SIZE
        end_y = math.ceil((self.editor.camera_y + visible_world_h) / settings.TILE_SIZE) * settings.TILE_SIZE

        for world_x in range(start_x, end_x + settings.TILE_SIZE, settings.TILE_SIZE):
            lx = int((world_x - self.editor.camera_x) * self.editor.zoom)
            pygame.draw.line(self.screen, (30, 35, 60), (lx, 0), (lx, grid_area))

        for world_y in range(start_y, end_y + settings.TILE_SIZE, settings.TILE_SIZE):
            ly = int((world_y - self.editor.camera_y) * self.editor.zoom)
            pygame.draw.line(self.screen, (25, 30, 55), (0, ly), (WIDTH, ly))

        for (ox, oy), obj_id in self.editor.objects.items():
            dx, dy = self.editor_world_to_screen(ox, oy)
            if -80 < dx < WIDTH and -120 < dy < grid_area:
                draw_rect = self.draw_editor_object(obj_id, (dx, dy))
                if self.editor.selected_object_pos == (ox, oy):
                    pygame.draw.rect(self.screen, (255, 240, 120), draw_rect.inflate(6, 6), width=3, border_radius=8)

        pygame.draw.rect(self.screen, settings.UI_BG, (0, grid_area, WIDTH, ui_h))

        btn_objects = pygame.Rect(18, grid_area + 16, 120, 44)
        btn_edit_mode = pygame.Rect(18, grid_area + 68, 120, 44)
        obj_color = settings.GREEN_BUTTON if self.editor.mode == "objects" else (60, 70, 110)
        edit_color = settings.GREEN_BUTTON if self.editor.mode == "edit" else (60, 70, 110)
        self.draw_button(btn_objects, "OBJECTS", obj_color)
        self.draw_button(btn_edit_mode, "EDIT", edit_color)

        undo_btn = pygame.Rect(WIDTH - 240, grid_area + 16, 60, 44)
        redo_btn = pygame.Rect(WIDTH - 170, grid_area + 16, 60, 44)
        self.draw_button(undo_btn, "<", (80, 110, 150))
        self.draw_button(redo_btn, ">", (80, 110, 150))

        btn_save = pygame.Rect(WIDTH - 115, 15, 100, 35)
        btn_test = pygame.Rect(WIDTH - 115, 60, 100, 35)
        self.draw_button(btn_save, "SALVAR", settings.GREEN_BUTTON)
        self.draw_button(btn_test, "TESTAR", settings.UI_ACCENT)

        name_txt = settings.FONT_HUD.render(self.editor.metadata.get("name", self.editor.level_name), True, settings.WHITE)
        desc_txt = settings.FONT_HUD.render(self.editor.metadata.get("description", "")[:38], True, settings.WHITE)
        zoom_txt = settings.FONT_HUD.render(f"ZOOM {int(self.editor.zoom * 100)}%", True, settings.WHITE)
        if self.editor.mode == "objects":
            hint_msg = "OBJECTS: escolha a aba, depois o objeto da paleta e clique no grid"
        else:
            hint_msg = "EDIT: clique no objeto e use Q/E/W/A/S/D | Ctrl+Z para desfazer"
        hint_txt = settings.FONT_HUD.render(hint_msg, True, settings.WHITE)
        self.screen.blit(name_txt, (15, 15))
        self.screen.blit(desc_txt, (15, 42))
        self.screen.blit(zoom_txt, (15, 69))
        self.screen.blit(hint_txt, (15, 96))

        palette_top = grid_area + 16
        palette_area = pygame.Rect(155, grid_area + 12, WIDTH - 420, ui_h - 24)

        if self.editor.mode == "objects":
            tabs = EDITOR_TABS
            tw = palette_area.width // len(tabs)
            for i, tab in enumerate(tabs):
                color = settings.UI_ACCENT if self.editor.current_tab == i else (50, 60, 100)
                tab_rect = pygame.Rect(palette_area.x + i * tw, palette_area.y, tw - 6, 34)
                pygame.draw.rect(self.screen, color, tab_rect, border_radius=10)
                self.screen.blit(settings.FONT_HUD.render(tab["label"], True, settings.WHITE), (tab_rect.x + 12, tab_rect.y + 8))

            items = self.editor.get_palette_items()
            palette_y = palette_area.y + 48
            item_w = 78
            for i, item in enumerate(items):
                item_rect = pygame.Rect(palette_area.x + i * (item_w + 10), palette_y, item_w, 78)
                selected = self.editor.selected_palette_index == i
                pygame.draw.rect(self.screen, (70, 88, 140) if selected else (44, 52, 84), item_rect, border_radius=12)
                preview = make_object_data(item, (0, 0))
                image_key = preview.get("image_key", infer_image_key(preview))
                src = settings.IMAGES[image_key]
                if preview.get("rotation", 0):
                    src = pygame.transform.rotate(src, preview["rotation"])
                thumb = pygame.transform.smoothscale(src, (38, 38))
                self.screen.blit(thumb, (item_rect.centerx - 19, item_rect.y + 8))
                label = settings.FONT_HUD.render(item["label"][:7], True, settings.WHITE)
                self.screen.blit(label, (item_rect.centerx - label.get_width() // 2, item_rect.bottom - 24))
        else:
            tool_area = pygame.Rect(155, grid_area + 16, 320, 120)
            for i, tool in enumerate(EDIT_TOOLS):
                row = i // 2
                col = i % 2
                tool_rect = pygame.Rect(tool_area.x + col * 155, tool_area.y + row * 54, 145, 44)
                active = self.editor.edit_tool == tool["key"]
                self.draw_button(tool_rect, tool["label"], settings.UI_ACCENT if active else (60, 70, 110))

            move_up = pygame.Rect(WIDTH - 340, grid_area + 78, 58, 38)
            move_left = pygame.Rect(WIDTH - 404, grid_area + 122, 58, 38)
            move_down = pygame.Rect(WIDTH - 340, grid_area + 122, 58, 38)
            move_right = pygame.Rect(WIDTH - 276, grid_area + 122, 58, 38)
            rot_left = pygame.Rect(WIDTH - 210, grid_area + 78, 82, 38)
            rot_right = pygame.Rect(WIDTH - 118, grid_area + 78, 82, 38)
            self.draw_button(move_up, "W", (65, 96, 135))
            self.draw_button(move_left, "A", (65, 96, 135))
            self.draw_button(move_down, "S", (65, 96, 135))
            self.draw_button(move_right, "D", (65, 96, 135))
            self.draw_button(rot_left, "Q", (90, 118, 90))
            self.draw_button(rot_right, "E", (90, 118, 90))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.editor.dragging = False
            if event.type == pygame.MOUSEMOTION and self.editor.dragging:
                dx, dy = event.rel
                self.editor.camera_x = max(0, self.editor.camera_x - (dx / self.editor.zoom))
                self.editor.camera_y = max(0, self.editor.camera_y - (dy / self.editor.zoom))
            if event.type == pygame.MOUSEWHEEL and pygame.key.get_mods() & pygame.KMOD_CTRL:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                old_zoom = self.editor.zoom
                world_x = self.editor.camera_x + (mouse_x / old_zoom)
                world_y = self.editor.camera_y + (min(mouse_y, grid_area) / old_zoom)
                self.editor.zoom = max(0.5, min(2.5, self.editor.zoom + (0.1 * event.y)))
                self.editor.camera_x = max(0, world_x - (mouse_x / self.editor.zoom))
                self.editor.camera_y = max(0, world_y - (min(mouse_y, grid_area) / self.editor.zoom))
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL
                if ctrl_pressed and event.button == 1 and my < grid_area:
                    self.editor.dragging = True
                elif btn_objects.collidepoint(mx, my):
                    self.editor.mode = "objects"
                elif btn_edit_mode.collidepoint(mx, my):
                    self.editor.mode = "edit"
                elif undo_btn.collidepoint(mx, my):
                    self.editor.undo()
                elif redo_btn.collidepoint(mx, my):
                    self.editor.redo()
                elif btn_save.collidepoint(mx, my):
                    self.lm.save(self.editor.level_name, self.editor.objects, self.editor.metadata, self.editor.folder)
                elif btn_test.collidepoint(mx, my):
                    self.start_level(self.export_editor_level_data(), "EDITOR_REAL")
                elif my < grid_area:
                    world_x = self.editor.camera_x + (mx / self.editor.zoom)
                    world_y = self.editor.camera_y + (my / self.editor.zoom)
                    gx = (int(world_x) // settings.TILE_SIZE) * settings.TILE_SIZE
                    gy = (int(world_y) // settings.TILE_SIZE) * settings.TILE_SIZE
                    if self.editor.mode == "objects":
                        if event.button == 1:
                            self.place_selected_palette_object((gx, gy))
                        if event.button == 3:
                            self.delete_editor_object((gx, gy))
                    else:
                        hit_pos, _ = self.get_editor_object_at(world_x, world_y)
                        if event.button == 1:
                            self.editor.selected_object_pos = hit_pos
                elif self.editor.mode == "objects":
                    items = self.editor.get_palette_items()
                    tabs = EDITOR_TABS
                    tw = palette_area.width // len(tabs)
                    for i, tab in enumerate(tabs):
                        tab_rect = pygame.Rect(palette_area.x + i * tw, palette_area.y, tw - 6, 34)
                        if tab_rect.collidepoint(mx, my):
                            self.editor.current_tab = i
                            self.editor.selected_palette_index = 0
                    palette_y = palette_area.y + 48
                    item_w = 78
                    for i, _item in enumerate(items):
                        item_rect = pygame.Rect(palette_area.x + i * (item_w + 10), palette_y, item_w, 78)
                        if item_rect.collidepoint(mx, my):
                            self.editor.selected_palette_index = i
                else:
                    tool_area = pygame.Rect(155, grid_area + 16, 320, 120)
                    for i, tool in enumerate(EDIT_TOOLS):
                        row = i // 2
                        col = i % 2
                        tool_rect = pygame.Rect(tool_area.x + col * 155, tool_area.y + row * 54, 145, 44)
                        if tool_rect.collidepoint(mx, my):
                            self.editor.edit_tool = tool["key"]

                    move_up = pygame.Rect(WIDTH - 340, grid_area + 78, 58, 38)
                    move_left = pygame.Rect(WIDTH - 404, grid_area + 122, 58, 38)
                    move_down = pygame.Rect(WIDTH - 340, grid_area + 122, 58, 38)
                    move_right = pygame.Rect(WIDTH - 276, grid_area + 122, 58, 38)
                    rot_left = pygame.Rect(WIDTH - 210, grid_area + 78, 82, 38)
                    rot_right = pygame.Rect(WIDTH - 118, grid_area + 78, 82, 38)
                    if move_up.collidepoint(mx, my):
                        self.move_selected_editor_object(0, -1)
                    elif move_left.collidepoint(mx, my):
                        self.move_selected_editor_object(-1, 0)
                    elif move_down.collidepoint(mx, my):
                        self.move_selected_editor_object(0, 1)
                    elif move_right.collidepoint(mx, my):
                        self.move_selected_editor_object(1, 0)
                    elif rot_left.collidepoint(mx, my):
                        self.rotate_selected_editor_object(90)
                    elif rot_right.collidepoint(mx, my):
                        self.rotate_selected_editor_object(-90)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.editor.camera_x += settings.TILE_SIZE * 2
                if event.key == pygame.K_LEFT:
                    self.editor.camera_x = max(0, self.editor.camera_x - settings.TILE_SIZE * 2)
                if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.editor.undo()
                self.handle_editor_key_action(event)
                if event.key == pygame.K_ESCAPE:
                    self.state = "EDITOR_SETUP"

    def play_scene(self):
        self.screen.fill(settings.BG_COLOR)
        self.screen.blit(settings.IMAGES["bg"], (0, 0))
        self.camera_x += 6
        self.player.hitbox.x = self.camera_x + 100
        self.all_sprites.update()

        self.resolve_solid_collisions()
        apply_portals(self)
        self.spawn_trail()
        self.update_particles()

        if self.touches_hazard() or self.player.hitbox.top > HEIGHT:
            self.spawn_death_burst()
            self.attempts += 1
            self.start_level(self.last_loaded_data, self.play_return_state)

        for sprite in self.all_sprites:
            if sprite is self.player:
                continue
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))

        self.draw_particles()
        self.screen.blit(self.player.image, (self.player.rect.x - self.camera_x, self.player.rect.y))

        prog = min(100, int((self.camera_x / max(1, self.level_width - WIDTH)) * 100))
        pygame.draw.rect(self.screen, (50, 50, 50), (WIDTH // 2 - 100, 30, 200, 12), border_radius=6)
        pygame.draw.rect(self.screen, settings.UI_ACCENT, (WIDTH // 2 - 100, 30, prog * 2, 12), border_radius=6)
        self.screen.blit(settings.FONT_HUD.render(f"ATTEMPT {self.attempts}", True, settings.WHITE), (20, 20))
        self.screen.blit(settings.FONT_HUD.render(f"{prog}%", True, settings.WHITE), (WIDTH // 2 + 110, 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = self.play_return_state

    def run(self):
        while self.running:
            if self.state == "MENU":
                self.menu_scene()
            elif self.state == "SELECT":
                self.select_scene()
            elif self.state == "PLAYING":
                self.play_scene()
            elif self.state == "EDITOR_MENU":
                self.editor_menu_scene()
            elif self.state == "EDITOR_SELECT":
                self.editor_select_scene()
            elif self.state == "EDITOR_SETUP":
                self.editor_setup_scene()
            elif self.state == "EDITOR_REAL":
                self.editor_real_scene()
            pygame.display.flip()
            self.clock.tick(settings.FPS)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
