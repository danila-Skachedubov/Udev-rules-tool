#!/usr/bin/env python3
import json
import os
import subprocess
from pydbus import SystemBus
import signal
import sys

class DconfWatcherDaemon:
    def __init__(self, path):
        self.dconf_path = path
        self.process = None

    def handle_change(self, change):
        print(f"Change detected: {change}")

    def start_watching(self):
        self.process = subprocess.Popen(
            ['dconf', 'watch', self.dconf_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        signal.signal(signal.SIGINT, self.stop_watching)
        signal.signal(signal.SIGTERM, self.stop_watching)

        try:
            while True:
                output = self.process.stdout.readline()
                if output:
                    self.handle_change(output.strip())
                elif self.process.poll() is not None:
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.cleanup()

    def stop_watching(self, signum, frame):
        print("Stopping the watcher...")
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        if self.process:
            self.process.terminate()
            self.process.wait()


class UdevApplier:
    json_dir = "/Software/BaseALT/Policies/Udev/"
    rules_dir = "/etc/udev/rules.d"

    def __init__(self):
        self.rules = {}

    def load_dict_from_dconf(self):
        try:
            result = subprocess.run(['dconf', 'dump', dconf_path], stdout=subprocess.PIPE)
            data = result.stdout.decode('utf-8')
            lines = data.strip().split('\n')
            current_key = None
            for line in lines:
                if line.startswith('['):
                    current_key = line.strip('[]')
                    self.rules [current_key] = {}
                elif line.startswith('rule='):
                    rule_str = line[len('rule='):]
                    rule_dict = eval(rule_str)
                    self.rules [current_key] = rule_dict
        except subprocess.CalledProcessError as e:
            print(f"Error reading from dconf: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from dconf data: {e}")

    def save_udev_rules(self):
        for rule_name, rule_data in self.rules.items():
            rule_filename = f'10-alt-policy-{rule_name}.rules'
            rule_filepath = os.path.join(self.rules_dir, rule_filename)
            if os.path.exists(rule_filepath):
                os.remove(rule_filepath)
                #print(f"Remove old file : {rule_filepath}")
            with open(rule_filepath, 'w') as rule_file:
                rule_lines = self.generate_udev_rule_lines(rule_data)
                rule_file.writelines(rule_lines)
                #print(f"Create new file : {rule_filepath}")

    def generate_udev_rule_lines(self, rule_data):
        rule_line = ""
        if isinstance(rule_data, list):
            for dict in rule_data:
                for key, value in dict.items():
                    rule_line += f"{key}\"{value}\", "
                rule_line = rule_line.strip(", ")
                rule_line += '\n'
        else:
            for key, value in rule_data.items():
                rule_line += f"{key}\"{value}\", "
            rule_line = rule_line.strip(", ")
        return rule_line

    def verify_udev_rules(self):
        wrong_files = []
        try:
            subprocess.run(
                ["/sbin/udevadm", "verify", f"{self.rules_dir}/",],
                check=True,
                text=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            if e.stderr:
                lines = e.stderr.splitlines()
                for i, line in enumerate(lines):
                    if line.startswith(self.rules_dir) and "udev rules check failed" in lines[i]:
                        error_report = line.split(":")[0]
                        wrong_files.append(error_report)
        print(wrong_files)
        self.remove_wrong_file(wrong_files)
        return wrong_files

    def remove_wrong_file(self, remove_list):
        for file_path in remove_list:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Удален файл: {file_path}")
                else:
                    print(f"Файл не найден: {file_path}")
            except Exception as e:
                print(f"Ошибка при удалении файла {file_path}: {e}")

    def get_systemd_version(self):
        try:
            bus = SystemBus()
            systemd = bus.get("org.freedesktop.systemd1")
            version = systemd.Version
            parts = version.split('.')
            return int(parts[0])
        except Exception as exc:
            print(exc)

if __name__ == '__main__':
    dconf_path = "/Software/BaseALT/Policies/Udev/"
    daemon = DconfWatcherDaemon(dconf_path)
    daemon.start_watching()