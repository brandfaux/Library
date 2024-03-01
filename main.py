from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'hello'

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Pass@123"
app.config['MYSQL_DB'] = "user_db"

mysql = MySQL(app)


def db_changes():
    mysql.connection.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
# this is login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # making connection
        cur = mysql.connection.cursor()

        check_if_in_db = cur.execute(
            "SELECT * FROM users WHERE username = '{user}' AND password = '{passs}'".format(user=username,
                                                                                            passs=password))

        if check_if_in_db == 1:
            session['user'] = username
            session.permanent = True
            return redirect('/inside')
    else:
        if 'user' in session:
            return redirect(url_for('home_user'))

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        user = request.form['username']
        passs = request.form['password']

        if passs == passs:

            cur1 = mysql.connection.cursor()
            check_user_duplicate = cur1.execute("SELECT * FROM users WHERE username= '{name}'".format(name=user))
            if check_user_duplicate > 0:
                return 'User already exists'

            else:
                cur1.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (user, passs))
                db_changes()
                return 'Register successfully'
        else:
            return 'Error not registered'
    return render_template('register.html')


@app.route('/inside')
def home_user():
    if 'user' in session:
        user = session['user']
        return f'Hello {user}'
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)