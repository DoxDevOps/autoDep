from flask import Flask, render_template, request, redirect, url_for, session, g
from multiprocessing import Process, Value
import time
import os
import sys
from flask import Response
from flask_sse import sse
from autodeploy import call_process
import sqlite3

# Global variables
process = None
clients = []

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        app_ctx = app.app_context()
        app_ctx.push()
        db = g._database = sqlite3.connect('database.sqlite')
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Perform authentication here using SQLite database
# Connect to the database


def redirect_output_to_db():
    db = get_db()
    # cursor = db.cursor()
    sys.stdout = DBOuput(db)

def restore_output():
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    

class DBOuput:
    def __init__(self, db):
        self.db = db
        self.create_table()

    def create_table(self):
        # Create the output_table if it doesn't exist
        query = "CREATE TABLE IF NOT EXISTS output_table (message TEXT)"
        self.db.execute(query)
        self.db.commit()

    def write(self, message):
        # Write the message to the database
        query = "INSERT INTO output_table (message) VALUES (?)"
        self.db.execute(query, (message,))
        self.db.commit()

    def flush(self):
        # Flush the output (if needed)
        pass



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
    # db = get_db()
    # cursor = db.cursor()
    redirect_output_to_db()
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
        with app.app_context():  # Set up the application context
            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT message FROM output_table")
            messages = cursor.fetchall()

            for message in messages:
                yield f"data: {message[0]}\n\n"

            # Close the cursor and database connection
            cursor.close()
            db.close()

            # Send the end_stream event
            yield "event: end_stream\ndata: End of stream\n\n"

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
    with app.app_context():
      app.run(host='0.0.0.0', debug=True)
