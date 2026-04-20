import json
import os

class LevelManager:
    def __init__(self):
        self.base = "levels"
        for f in ["main", "custom"]:
            os.makedirs(os.path.join(self.base, f), exist_ok=True)

    def save(self, name, objects_dict, metadata, folder="custom"):
        # Converte {(x,y): "id,sub"} em lista para JSON
        obj_list = []
        for (x, y), val in objects_dict.items():
            parts = val.split(',')
            obj_list.append({"id": parts[0], "x": x, "y": y, "type": parts[2] if len(parts)>2 else None})
        
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