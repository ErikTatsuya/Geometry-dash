import json
from world.objects.block import Block

class Level:
    def __init__(self, path):
        self.objects = []

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.metadata = data["metadata"]

        for obj in data["objects"]:
            self.create_object(obj)

    def create_object(self, obj):
        obj_id = obj["id"]
        x = obj["x"]
        y = obj["y"]
        rotation = obj.get("rotation", 0)

        if obj_id == "block":
            self.objects.append(Block(x, y, rotation))

    def update(self):
        for obj in self.objects:
            obj.update()