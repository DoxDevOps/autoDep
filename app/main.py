from flask import Flask, render_template, request, redirect, url_for, session
from multiprocessing import Process, Value
import time
import os
from flask import Response
from flask_sse import sse
from autodeploy import call_process

# Global variables
process = None
clients = []

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
                session['process_running'] = True
                start_process()
            elif 'stop' in request.form:
                session['process_running'] = False
                stop_process()

        return render_template('landing.html', process_running=session.get('process_running', False))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

def get_output_path():
    # Get the directory path of the code file
    dir_path = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(dir_path, 'output.txt')
    return output_path

def start_process():
    session['process_started'] = True
    
    global process
    if process is None or not process.is_alive():
        # Start the process if it's not already running or terminated
        process = Process(target=call_process)
        process.start()
        session['process_running'] = True

def stop_process():
    session['process_started'] = False
    # Your code to stop the process

    # Terminate the process that monitors output changes
    global process
    if process:
        process.terminate()
        process.join()
        process = None


def send_output_changes(content):
    # Iterate over connected clients and send the content to each client
    for client in clients:
        client.put(content)

def read_output_changes():
    output_path = get_output_path()
    
    with open(output_path, 'r') as file:
        text = file.read()
    
    return text

@app.route('/output_stream')
def output_stream():
    def stream():
        with open(get_output_path(), 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                yield 'data: {}\n\n'.format(line.strip())

    # Return the SSE response
    
    return Response(stream(), mimetype='text/event-stream')


def get_file_changes():
    try:
        with open(get_output_path(), 'r') as file:
            lines = file.readlines()

            print(len(lines))

        # Check if the file has been modified
        if len(lines) == 0:
            return "No changes made to the file."

        changes = []
        for line in lines[-1:]:
            line = line.strip()
            if line:
                changes.append(line)

        if len(changes) == 0:
            return "No changes made to the file."

        return changes

    except FileNotFoundError:
        return "File not found."

def stream_file_changes():
    while True:
        changes = get_file_changes()

        if isinstance(changes, str):
            yield f"data: {changes}\n\n"
        else:
            for change in changes:
                yield f"data: {change}\n\n"

        # Sleep for a specified interval (e.g., 1 second)
        time.sleep(1)

@app.route('/output_current_stream')
def output_current_stream():
    return Response(stream_file_changes(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)
