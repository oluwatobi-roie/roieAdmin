from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from requests.auth import HTTPBasicAuth
import json

login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # get data from the login form
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate with Traccar API
        traccar_api_url = 'https://track.roie.com.ng/api/session'
        traccar_payload = {'email': username, 'password': password}
        traccar_response = requests.post(traccar_api_url, data=traccar_payload, auth=HTTPBasicAuth(username, password))


        if traccar_response.status_code == 200:
            session_cookie = traccar_response.cookies.get('JSESSIONID')
            session['traccar_session_cookie'] = session_cookie

            traccar_data = traccar_response.json()

            print(traccar_data) #this is for debug
            
            devices_api_url = f'https://track.roie.com.ng/api/devices'
            traccar_apiHeader = {'Cookie': f'JSESSIONID={session_cookie}'}
            devices_response = requests.get(devices_api_url, headers=traccar_apiHeader)

            if devices_response.status_code == 200:
                devices_data = devices_response.json()
                for i in devices_data:
                    print(i['name'])
            return redirect(url_for('index', username = 'username'))
        else:
            return render_template('index.html', error='Invalid Credentials')
    return render_template('index.html')





@logout_bp.route('/logout')
def logout():
    session.pop('traccar_session_cookie', None)
    return redirect(url_for('index'))
