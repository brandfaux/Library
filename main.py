from flask import Flask, request, redirect, url_for, session, render_template
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@123",
    database="user_db"
)
cursor = db.cursor()

# Function to authenticate user
def authenticate(username, password):
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    return user

@app.route('/')
def home():
    if 'username' in session:
        return f"Logged in as {session['username']}<br><a href='/logout'>Logout</a>"
    return "You are not logged in<br><a href='/login'>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
