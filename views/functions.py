import requests 
from flask import session, Blueprint, request, render_template, jsonify
from touch import roie_endpoint as endpoint, getOneYearDate, randomPassword, notification_wizard
from sqlScripts import assign_user_notification, search_user, link_device_user
from views.utils import get_devices



# declare some global variables that wwil be used here. 
devices_api_url = f'{endpoint}devices'
user_api_url = f'{endpoint}users'
notification_api_url = f'{endpoint}notifications'

# blueprint for our add device url
adddevice_bp = Blueprint('add_device', __name__)
reg_user_bp = Blueprint('reg_user', __name__)
check_user_bp = Blueprint('check_user', __name__)
link_user_bp = Blueprint('link_user', __name__)


@adddevice_bp.route('/add_device', methods=['POST'])
def add_device():
    session_cookie = session.get('traccar_session_cookie')
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


@reg_user_bp.route('/reg_user', methods=['POST'])
def reg_user():
    session_cookie = session.get('traccar_session_cookie')
     # check if a session currently exist
    
    if 'traccar_session_cookie' in session:
        if request.method == 'POST':
            traccar_api_headers = {'Cookie': f'JSESSIONID = {session_cookie}'}

            default_atribute = {
                "mapLiveRoutes":"selected",
                "mapFollow":"true",
                "deviceSecondary":"phone",
                "activeMapStyles":",googleRoad,googleSatellite,googleHybrid,custom",
                "positionItems":"speed,address,motion,ignition,fixTime,deviceTime,alarm,blocked"
            }
            data = {
                'name': request.json.get('name'),
                'email': request.json.get('email'),
                'phone': request.json.get('phone'),
                'fixedEmail': 'true',
                'deviceReadonly': 'true',
                'expirationTime': getOneYearDate(),
                'password': randomPassword(8),
                'attributes': default_atribute,
                }
            
            # Send mapped devices to traccar api
            response = requests.post(user_api_url, json=data, headers=traccar_api_headers)


            # Check the Traccar API response
            if response.status_code == 200:
                # create a list of all the notification that will be created for this session
                notification_id_list = []

                # save the userID that has just been created in a variable
                user_id = response.json().get('id')
                print(f"User Successfully Created with ID: {user_id}")

                # List all the notification that are of interest to us
                notification_lists = ['ignitionOn', 'ignitionOff', 'geofenceExit', 'geofenceEnter', 'alarm']
                # notification_lists = ['ignitionOn', 'ignitionOff']


                for i in notification_lists:
                    response = requests.post(notification_api_url, json=notification_wizard(i), headers=traccar_api_headers)
                    
                    # save the ID's of all the notification created for sql to move
                    notification_id = response.json().get('id')
                    notification_id_list.append(notification_id)
                    print(f"{i} Notification Created with ID {notification_id}")
                print(notification_id_list)


                assign_user_notification(user_id, notification_id_list)
                return response.json()  # or any other desired 
                
            else:
                return f'Add User Error: {response.status_code} - {response.text}'
            
        return None
    return render_template('index.html')


@check_user_bp.route('/check_user', methods=['POST'])
def check_user():
    if 'traccar_session_cookie' in session:
        data = request.get_json()
        email = data.get('email', '')
        
        userFound, user_id = search_user(email)

        if userFound:
            code = "12345"
            response = {'exists': True, 'verification_code': code, 'user_id': user_id}
        else:
            response = {'exists': False, 'verification_code': None, 'user_id': None}

    return jsonify(response)
    
    # return render_template('index.html')


@link_user_bp.route('/link_user', methods=['POST'])
def link_user():
    data = request.get_json()
    userid = data.get('userid', '')
    deviceid = data.get('deviceid', '')
    if (link_device_user(userid, deviceid)):
        response = {'success': True}
    else:
        response = {'success': None}
    
    return jsonify(response)