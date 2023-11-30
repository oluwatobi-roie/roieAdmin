from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from requests.auth import HTTPBasicAuth


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
            traccar_data = traccar_response.json()
            session_cookie = traccar_response.cookies.get('JSESSIONID')
            session['traccar_session_cookie'] = session_cookie
            session['traccar_logged_user'] = traccar_data['name']
            
            print(traccar_data['name']) #this is for debug

            return redirect(url_for('index'))
        else:
            return render_template('index.html', error='Invalid Credentials')
    return render_template('index.html')





@logout_bp.route('/logout')
def logout():
    session.pop('traccar_session_cookie', None)
    return redirect(url_for('index'))
