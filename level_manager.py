import json
import os

class LevelManager:
    def __init__(self):
        self.base = "levels"
        for f in ["main", "custom"]:
            os.makedirs(os.path.join(self.base, f), exist_ok=True)

    def save(self, name, objects_dict, metadata, folder="custom"):
        obj_list = []
        for (x, y), val in objects_dict.items():
            if isinstance(val, dict):
                obj = {"id": val["id"], "x": x, "y": y}
                if val.get("type"):
                    obj["type"] = val["type"]
                if val.get("rotation", 0):
                    obj["rotation"] = val["rotation"] % 360
            else:
                parts = val.split(',')
                obj = {"id": parts[0], "x": x, "y": y}
                if len(parts) > 1 and parts[1]:
                    obj["type"] = parts[1]
            obj_list.append(obj)
        
        data = {"metadata": metadata, "objects": obj_list}
        with open(f"{self.base}/{folder}/{name}.json", 'w') as f:
            json.dump(data, f, indent=4)

    def load(self, name, folder="custom"):
        path = f"{self.base}/{folder}/{name}.json"
        if not os.path.exists(path): return None
        with open(path, 'r') as f:
            return json.load(f)

    def list_files(self, folder):
        return [f.replace('.json', '') for f in os.listdir(f"{self.base}/{folder}") if f.endswith('.json')]
