from datetime import datetime
import requests
from flask import session
from touch import roie_endpoint as endpoint
# from touch import api

devices_api_url = f'{endpoint}devices'
    
def get_devices(session_cookie):
    traccar_apiHeader = {'Cookie': f'JSESSIONID={session_cookie}'}
    devices_response = requests.get(devices_api_url, headers=traccar_apiHeader)
    if devices_response.status_code == 200:
        devices_data = devices_response.json()
        return devices_data
    else:
        return None
    
def get_geofence(id):
    # declare variables to uses in this function
    position_api_url = f'{endpoint}positions?'
    geofence_api_url = f'{endpoint}geofences'
    session_cookie = session.get('traccar_session_cookie')

    # header for position API
    traccar_apiHeader = {
        'Cookie': f'JSESSIONID={session_cookie}',
        'Accept': 'application/json',
        }
    
    # data passed in the position api function, id is position ID
    data = {
        'id': id,
    }

    # response from the position API
    position_response = requests.get(position_api_url, params=data, headers=traccar_apiHeader)
    if position_response.status_code == 200:

        position_data = position_response.json()
        # print(position_data)
        
        geofenceId = position_data[0]['geofenceIds']
        if type(geofenceId) is list:
            # call geofence api to get the name
            allGeofences = requests.get(geofence_api_url, headers=traccar_apiHeader)
            for Geo_id in allGeofences.json():
                if Geo_id['id'] == geofenceId[0]:
                    return Geo_id['name']
        else:
            return None
    else:
        print(position_response.status_code, " Error")
        return None

def fromIsotoString(isoFormat):
    date_time = datetime.fromisoformat(isoFormat.replace('Z', '+00:00'))

    # Format the date and time
    formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_date_time

def fromMillisectoSec(duration):
    duration = duration/1000
    days, remainder = divmod(duration, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    duration_string = ""
    if days > 0:
        duration_string += f"{int(days)} days, "
    if hours > 0:
        duration_string += f"{int(hours)} hours, "
    if minutes > 0:
        duration_string += f"{int(minutes)} minutes, "
    if seconds > 0:
        duration_string += f"{int(seconds)} seconds"

    return duration_string
