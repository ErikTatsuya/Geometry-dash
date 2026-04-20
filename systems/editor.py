import copy
import pygame


EDITOR_TABS = [
    {
        "key": "blocks",
        "label": "BLOCKS",
        "items": [
            {"label": "Block", "id": "1", "image_key": "block", "rotation": 0},
            {"label": "Slope R", "id": "5", "image_key": "slope", "rotation": 0},
            {"label": "Slope L", "id": "5", "image_key": "slope", "rotation": 180},
        ],
    },
    {
        "key": "spikes",
        "label": "SPIKES",
        "items": [
            {"label": "Spike Up", "id": "2", "image_key": "spike", "rotation": 0},
            {"label": "Spike Right", "id": "2", "image_key": "spike", "rotation": 270},
            {"label": "Spike Down", "id": "2", "image_key": "spike", "rotation": 180},
            {"label": "Spike Left", "id": "2", "image_key": "spike", "rotation": 90},
        ],
    },
    {
        "key": "saws",
        "label": "SAWS",
        "items": [
            {"label": "Saw", "id": "3", "image_key": "saw", "rotation": 0},
        ],
    },
    {
        "key": "portals",
        "label": "PORTALS",
        "items": [
            {"label": "Ship", "id": "4", "image_key": "p_ship", "type": "s", "rotation": 0},
            {"label": "Cube", "id": "4", "image_key": "p_cube", "type": "c", "rotation": 0},
            {"label": "Grav -", "id": "4", "image_key": "p_grav", "type": "gi", "rotation": 0},
            {"label": "Grav +", "id": "4", "image_key": "p_grav", "type": "gn", "rotation": 0},
            {"label": "Wave", "id": "4", "image_key": "p_wave", "type": "w", "rotation": 0},
        ],
    },
]


EDIT_TOOLS = [
    {"key": "select", "label": "SELECT"},
    {"key": "move", "label": "MOVE"},
    {"key": "rotate_left", "label": "ROT L"},
    {"key": "rotate_right", "label": "ROT R"},
]


def make_object_data(item, grid_pos):
    data = {
        "id": item["id"],
        "x": grid_pos[0],
        "y": grid_pos[1],
        "rotation": item.get("rotation", 0) % 360,
    }
    if "type" in item:
        data["type"] = item["type"]
    if "image_key" in item:
        data["image_key"] = item["image_key"]
    return data


def clone_object(data):
    return copy.deepcopy(data)


class EditorState:
    def __init__(self):
        self.objects = {}
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        self.dragging = False
        self.current_tab = 0
        self.level_name = "novo_nivel"
        self.folder = "custom"
        self.metadata = {"name": "novo_nivel", "description": "", "music": ""}
        self.form_active = "name"
        self.pending_open = None
        self.mode = "objects"
        self.edit_tool = "select"
        self.selected_palette_index = 0
        self.selected_object_pos = None
        self.undo_stack = []
        self.redo_stack = []

    def reset(self, level_name="novo_nivel", folder="custom", metadata=None):
        self.objects = {}
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        self.dragging = False
        self.current_tab = 0
        self.level_name = level_name
        self.folder = folder
        self.metadata = {"name": level_name, "description": "", "music": ""}
        if metadata:
            self.metadata.update(
                {
                    "name": metadata.get("name", level_name),
                    "description": metadata.get("description", ""),
                    "music": metadata.get("music", ""),
                }
            )
        self.form_active = "name"
        self.pending_open = None
        self.mode = "objects"
        self.edit_tool = "select"
        self.selected_palette_index = 0
        self.selected_object_pos = None
        self.undo_stack = []
        self.redo_stack = []

    def get_current_tab(self):
        return EDITOR_TABS[self.current_tab]

    def get_palette_items(self):
        return self.get_current_tab()["items"]

    def get_selected_palette_item(self):
        items = self.get_palette_items()
        return items[min(self.selected_palette_index, len(items) - 1)]

    def load_level_data(self, level_name, folder, data):
        self.reset(level_name, folder, data.get("metadata", {}))
        for obj in data.get("objects", []):
            loaded = {
                "id": obj["id"],
                "x": obj["x"],
                "y": obj["y"],
                "rotation": obj.get("rotation", 0) % 360,
                "type": obj.get("type"),
            }
            loaded["image_key"] = infer_image_key(loaded)
            self.objects[(loaded["x"], loaded["y"])] = loaded
        self.pending_open = (level_name, folder)

    def export_level_data(self):
        objects = []
        for pos, value in self.objects.items():
            obj = {"id": value["id"], "x": pos[0], "y": pos[1]}
            if value.get("type"):
                obj["type"] = value["type"]
            if value.get("rotation", 0):
                obj["rotation"] = value["rotation"] % 360
            objects.append(obj)
        return {"metadata": dict(self.metadata), "objects": objects}

    def snapshot(self):
        return {
            "objects": copy.deepcopy(self.objects),
            "selected_object_pos": self.selected_object_pos,
        }

    def push_undo(self):
        self.undo_stack.append(self.snapshot())
        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return False
        self.redo_stack.append(self.snapshot())
        snap = self.undo_stack.pop()
        self.objects = snap["objects"]
        self.selected_object_pos = snap["selected_object_pos"]
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        self.undo_stack.append(self.snapshot())
        snap = self.redo_stack.pop()
        self.objects = snap["objects"]
        self.selected_object_pos = snap["selected_object_pos"]
        return True


def infer_image_key(obj):
    if obj["id"] == "1":
        return "block"
    if obj["id"] == "2":
        return "spike"
    if obj["id"] == "3":
        return "saw"
    if obj["id"] == "5":
        return "slope"
    if obj["id"] == "4":
        mapping = {"s": "p_ship", "w": "p_wave", "c": "p_cube", "gi": "p_grav", "gn": "p_grav"}
        return mapping.get(obj.get("type", "s"), "p_ship")
    return "block"


def draw_text_input(screen, font, accent, white, rect, label, field_name, editor_state):
    active = editor_state.form_active == field_name
    color = (68, 84, 135) if active else (39, 45, 70)
    border = accent if active else (85, 96, 140)
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, border, rect, width=2, border_radius=12)
    screen.blit(font.render(label, True, white), (rect.x, rect.y - 24))

    text = editor_state.metadata.get(field_name, "")
    display = text if text else "..."
    screen.blit(font.render(display, True, white), (rect.x + 12, rect.y + 12))
