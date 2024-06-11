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
                        for rule_name, rule_data in data.items():
                            self.rules[rule_name] = rule_data
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from file {file_path}: {e}")
            else:
                print(f"No json files were found in the {self.json_dir} directory ")

    def save_udev_rules(self):
        for rule_name, rule_data in self.rules.items():
            rule_filename = f'10-alt-policy-{rule_name}.rules'
            rule_filepath = os.path.join(self.rules_dir, rule_filename)
            if os.path.exists(rule_filepath):
                os.remove(rule_filepath)
                #print(f"Remove old file : {rule_filepath}")
            with open(rule_filepath, 'w') as rule_file:
                rule_lines = self.generate_udev_rule_lines(rule_data)
                #rule_file.writelines(rule_lines)
                #print(f"Create new file : {rule_filepath}")

    def generate_udev_rule_lines(self, rule_data):
        rule_line = ""
        print('rule_data----', rule_data)
        if isinstance(rule_data, list):
            for dict in rule_data:
                for key, value in dict.items():
                    rule_line += f"{key}\"{value}\", "
                rule_line += '\n'
        else:
            for key, value in rule_data.items():
                rule_line += f"{key}{value}, "
            print(rule_line)

if __name__ == '__main__':
    applier = UdevApplier()
    applier.load_json_files()
    applier.save_udev_rules()
