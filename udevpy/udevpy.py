import json
import os

class UdevApplier:
    json_dir = "/etc/udev/json"

    def __init__(self):
        self.rules = {}

    def load_json_files(self):
        for filename in os.listdir(self.json_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.json_dir, filename)
                with open(file_path, 'r') as file:
                    try:
                        data = json.load(file)
                        self.rules.update(data)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {file_path}: {e}")




if __name__ == '__main__':
    applier = UdevApplier()
    applier.load_json_files()