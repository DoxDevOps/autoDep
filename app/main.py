from flask import Flask, render_template, request, redirect, url_for, session
from multiprocessing import Process, Value
from autodeploy import init

process = None

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform authentication here
        # For simplicity, let's assume the username is "admin" and the password is "password"
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('landing'))

        return render_template('login.html', message='Invalid credentials')

    return render_template('login.html')

@app.route('/landing', methods=['GET', 'POST'])
def landing():
    if 'logged_in' in session and session['logged_in']:
        if request.method == 'POST':
            if 'start' in request.form:
                start_process()
            elif 'stop' in request.form:
                stop_process()

        process_running_value = process.is_alive() if process is not None else False
        return render_template('landing.html', process_running=process_running_value)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def start_process():
    global process

    if process is None or not process.is_alive():
        # Start the process if it's not already running or terminated
        process = Process(target=init)
        process.start()
        session['process_running'] = True

def stop_process():
    global process

    if process is not None and process.is_alive():
        # Stop the process if it's running
        process.terminate()
        process.join()
        session['process_running'] = False

if __name__ == '__main__':
    app.run(debug=True)
