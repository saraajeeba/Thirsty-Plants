from flask import Flask, render_template, request, redirect, url_for
import os, time

app = Flask(__name__)

USER_EMAIL_FILE = 'user_email.txt'
STATUS_FILE = 'rain_status.txt'

@app.route('/', methods=['GET'])
def index():
    email = ""
    if os.path.exists(USER_EMAIL_FILE):
        with open(USER_EMAIL_FILE, 'r') as f:
            email = f.read().strip()
    return render_template('input.html', email=email)

@app.route('/submit_email', methods=['POST'])
def submit_email():
    email = request.form.get('email', "").strip()
    if not email:
        return "Invalid email", 400
    with open(USER_EMAIL_FILE, 'w') as f:
        f.write(email) 
    return redirect(url_for('status'))

@app.route('/status', methods=['GET'])
def status():
    status = 'Unknown'
    last = 'Never'
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            status = f.read().strip()
        last = time.ctime(os.path.getmtime(STATUS_FILE))
    return render_template('status.html', status=status, last=last)

if __name__ == '__main__':
    app.run(debug=True)