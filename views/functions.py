import requests 
from flask import session, Blueprint, request, render_template
from touch import roie_endpoint as endpoint
from views.utils import get_devices


# declare some global variables that wwil be used here. 
devices_api_url = f'{endpoint}devices'

# blueprint for our add device url
adddevice_bp = Blueprint('add_device', __name__)

@adddevice_bp.route('/add_device', methods=['POST'])
def add_device():
    session_cookie = session.get('traccar_session_cookie')
    print(session_cookie)
    # check if a session currently exist

    if 'traccar_session_cookie' in session:
        if request.method == 'POST':
            traccar_api_headers = {'Cookie': f'JSESSIONID = {session_cookie}'}
            data = {
                'name': request.json.get('plateNumber'),
                'uniqueId': request.json.get('uniqueId'),
                'phone': request.json.get('devicePhone'),
                'category': request.json.get('category'),
                    }
            
            # Send mapped devices to traccar api

            response = requests.post(devices_api_url, json=data, headers=traccar_api_headers)
            print (devices_api_url)
            print(response)
            # Check the Traccar API response
            if response.status_code == 200:
                get_devices(session_cookie)
                return response.json()  # or any other desired response
                
            else:
                return f'Error: {response.status_code} - {response.text}'
            
        return None
    return render_template('index.html')    
