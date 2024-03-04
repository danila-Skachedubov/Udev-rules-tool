import json


def process_parameters(json_data):

     try:
          data = json.loads(json_data)
          action = data.get('ACTION')
          subsystem = data.get('SUBSYSTEM')
          rule = data.get('RULE')
          parameters = {key: value for key, value in data.items() if key not in ['ACTION', 'SUBSYSTEM', 'RULE']}

          create_udev_rule(action, subsystem, rule, parameters)

     except Exception as exc:
          print(exc)

def create_udev_rule(action, subsystem, rule, parameters):
     pass