import requests
from touch import roie_endpoint as endpoint


def get_devices(session_cookie):
    devices_api_url = f'{endpoint}/devices'
    traccar_apiHeader = {'Cookie': f'JSESSIONID={session_cookie}'}
    devices_response = requests.get(devices_api_url, headers=traccar_apiHeader)
    if devices_response.status_code == 200:
        devices_data = devices_response.json()
        return devices_data
    else:
        return None