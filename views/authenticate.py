from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
from requests.auth import HTTPBasicAuth


login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get data from the login form
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate with Traccar API
        traccar_api_url = 'https://track.roie.com.ng/api/session'
        traccar_payload = {'email': username, 'password': password}
        traccar_response = requests.post(traccar_api_url, data=traccar_payload, auth=HTTPBasicAuth(username, password))

        # Check if uthentication was successfull. 
        if traccar_response.status_code == 200:
            #get and save Traccar session to allow persistent authentication as traccar_session_cookie
            session_cookie = traccar_response.cookies.get('JSESSIONID')
            session['traccar_session_cookie'] = session_cookie

            #extract name and id of the content from the session api
            traccar_data = traccar_response.json()
            session['user_name'] = traccar_data.get('name')
            session['user_id'] = traccar_data.get('id')


            return redirect(url_for('index'))
        else:
            return render_template('index.html', error='Invalid Credentials')
    return render_template('index.html')





@logout_bp.route('/logout')
def logout():
    # loops through each sessions stored in flask and pop them all out. 
    for x in list(session.keys()):
        session.pop(x, None)
    return redirect(url_for('index'))
