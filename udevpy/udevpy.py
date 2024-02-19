import json

def process_parameters(selected_device, selected_action, parameters):
    data = {
        'Selected Device': selected_device,
        'Selected Action': selected_action,
        'Parameters': parameters
    }

    print(f'Processing saved parameters:')
    print(f'Selected Device: {data["Selected Device"]}')
    print(f'Selected Action: {data["Selected Action"]}')
    print(f'Parameters: {json.dumps(data["Parameters"], indent=4)}')