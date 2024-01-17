from touch import myKey as myKey #this is unique to my code to import my flask app key
from flask import Flask, session, render_template
from views.authenticate import login_bp, logout_bp
from views.functions import adddevice_bp, reg_user_bp, check_user_bp, link_user_bp
from views.reportParking import parkingreport_bp
from views.utils import get_devices


app = Flask(__name__)
app.secret_key = myKey

app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(adddevice_bp)
app.register_blueprint(reg_user_bp)
app.register_blueprint(check_user_bp)
app.register_blueprint(link_user_bp)
app.register_blueprint(parkingreport_bp)


@app.route('/')
def index():
    if 'traccar_session_cookie' in session:
        devices_data = get_devices(session['traccar_session_cookie'])
        user_name = session.get('user_name')
        user_id = session.get('user_id')
        if devices_data:
            return render_template('dashboard.html', devices_data=devices_data, user_name=user_name, user_id=user_id )
        else:
            return render_template('dashboard.html', error='Error fetching devices')
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)