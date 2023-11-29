from flask import Flask, session, render_template
from views.authenticate import login_bp, logout_bp
from touch import myKey #this is unique to my code to import my flask app key

app = Flask(__name__)
app.secret_key = myKey

app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)

@app.route('/')
def index():
    if 'traccar_session_cookie' in session:
        return render_template('Dashboard.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)