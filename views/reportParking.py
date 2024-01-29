from datetime import datetime, timedelta, timezone
from flask import Blueprint, session, request
import requests
from touch import roie_endpoint as endpoint
from views.utils import get_devices, get_geofence, fromIsotoString, fromMillisectoSec


parkingreport_bp = Blueprint('parking_report', __name__)
@parkingreport_bp.route('/report-parking', methods=["GET"])
def parking_report():
    stop_report_api_url = f'{endpoint}reports/stops?'
    session_cookie = session.get('traccar_session_cookie')
    # check if a session currently exist
    
    if 'traccar_session_cookie' in session:
        if request.method == 'GET':
            traccar_api_headers = {
                'Cookie': f'JSESSIONID = {session_cookie}',
                'Accept': 'application/json',
                }
            current_datetime = datetime.now(timezone.utc)
            one_week_ago = current_datetime - timedelta(days=7)
            
            devices_data = get_devices(session['traccar_session_cookie'])
            deviceID = []

            for i in devices_data:
                deviceID.append(i['id'])

            data = {
                # 'deviceId': deviceID[3],	
                'deviceId': 1046,
                'from': one_week_ago.replace(tzinfo=timezone.utc).isoformat(),
                'to': current_datetime.replace(tzinfo=timezone.utc).isoformat(),
           }
            

            
            stop_response = requests.get(stop_report_api_url, params=data, headers=traccar_api_headers)
            # Check the Traccar API response

            formated_data = []
            if stop_response.status_code == 200:
                response_data = stop_response.json()
                for items in response_data:
                    geofence_name = get_geofence(items['positionId'])

                    # check if geofence_name exist and then replace the name with geofence name
                    if geofence_name is not None:
                        items['address'] = geofence_name

                    # reduce the amount of data sent to front end by only sending actual data required. 
                    formated_item = {
                        'deviceId': items['deviceId'],
                        'deviceName': items['deviceName'],
                        'address': items['address'],
                        'startTime': fromIsotoString(items['startTime']),
                        'endTime': fromIsotoString(items['endTime']),
                        'duration': fromMillisectoSec(items['duration'])
                    }

                    formated_data.append(formated_item)
                # print(response_data)
                return formated_data
            else:
                return f'Error: {stop_response.status_code} - {stop_response.text}'
        return None
    # return render_template('index.html')
