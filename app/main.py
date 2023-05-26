from flask import Flask, render_template, request, redirect, url_for, session

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

@app.route('/landing')
def landing():
    if 'logged_in' in session and session['logged_in']:
        return render_template('landing.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
