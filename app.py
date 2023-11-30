from flask import Flask, session, render_template
from views.authenticate import login_bp, logout_bp
from touch import myKey #this is unique to my code to import my flask app key
from utils import get_devices


app = Flask(__name__)
app.secret_key = myKey

app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)

@app.route('/')
def index():
    if 'traccar_session_cookie' in session:
        devices_data = get_devices(session['traccar_session_cookie'])

        if devices_data:
            return render_template('dashboard.html', devices_data=devices_data, )
        else:
            return render_template('dashboard.html', error='Error fetching devices')
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)