import os
import json
from settings import *

def load_levels(levels_path):
    levels = []

    if not levels_path.exists():
        print("Pasta 'levels' não encontrada")
        return levels

    for file in os.listdir(levels_path):
        if file.endswith(".json"):
            path = levels_path / file

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

                levels.append({
                    "file": file,
                    "path": levels_path / path,
                    "data": data
                })

    return levels