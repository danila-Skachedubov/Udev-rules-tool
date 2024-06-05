import json
import os

class UdevApplier:
    json_dir = "/etc/udev/json"
    rules_dir = "/etc/udev/rules.d"

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

    def save_udev_rules(self):
        for rule_name, rule_data in self.rules.items():
            rule_filename = f'10-policy-{rule_name}.rules'
            rule_filepath = os.path.join(self.rules_dir, rule_filename)
            if os.path.exists(rule_filepath):
                os.remove(rule_filepath)
                print(f"Удален старый файл : {rule_filepath}")

if __name__ == '__main__':
    applier = UdevApplier()
    applier.load_json_files()
    applier.save_udev_rules()
