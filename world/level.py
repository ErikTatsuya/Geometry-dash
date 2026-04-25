import json
from world.registry import OBJECT_TYPES
from world.objects.block import Block

class Level:
    def __init__(self, path):
        self.objects = []
        self.metadata = {}

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.metadata = data.get("metadata", {})
        self.load_objects(data.get("objects", []))

    def load_objects(self, objects_data):
        for obj in objects_data:
            self.create_object(obj)

    def create_object(self, obj):
        obj_id = obj.get("id")
        x = obj.get("x", 0)
        y = obj.get("y", 0)
        rotation = obj.get("rotation", 0)

        image_path = OBJECT_TYPES.get(obj_id)

        if image_path is None:
            print(f"ID desconhecido no level.py: {obj_id}")
            return

        self.objects.append(Block(x, y, image_path, rotation))

    def update(self):
        for obj in self.objects:
            obj.update()

    def get_solids(self):
        return [obj for obj in self.objects if hasattr(obj, "rect")]