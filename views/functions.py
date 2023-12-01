# import requests 
from flask import session, Blueprint, request, render_template
from touch import roie_endpoint as endpoint
# from touch import api

devices_api_url = f'{endpoint}/devices'

# blueprint for our add device url
adddevice_bp = Blueprint('add_device', __name__)

@adddevice_bp.route('/add_device', methods=['POST'])
def add_device():
    session_cookie = session.get('traccar_session_cookie')
    if 'traccar_session_cookie' in session:
        if request.method == 'POST':
            devcice_api_url = f'{endpoint}/devices'
            traccar_apiHeader = {'Cookie': f'JSESSINOID = {session_cookie}'}
            data = request.json
            print(data)
            return data
        return None
    return render_template('index.html')    
