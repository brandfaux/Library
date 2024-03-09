from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_scss import Scss

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

@app.route('/user/<name>')
def user(name):
    return render_template("taps.html", user_name=name)

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

@app.route('/registration_not_found')
def registration_not_found():
    # Render a page indicating that PRN was not found
    return render_template('prn_not_found.html')
@app.route('/inside')
def home_user():
    if 'user' in session:
        user = session['user']
        return render_template('user.html', username=user)
    else:
        return redirect(url_for('login'))

# New route for PRN search
from flask import render_template

@app.route('/search_prn', methods=['POST', 'GET'])
def search_prn():
    if request.method == 'POST':
        prn_no = request.form['prn_no']
        cur = mysql.connection.cursor()
        cur.execute("SELECT name FROM prn WHERE full_prn = %s", (prn_no,))
        result = cur.fetchone()
        cur.close()

        if result:
            name = result[0]  # Extracting the name from the result
            flash('Name: {}'.format(name))
            return render_template('name.html', name=name)  # Pass the name as a variable to the template
        else:
            return render_template('search.html')
    else:
        return render_template('search.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

#custom error pages

#Invalid URL

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#internal server error

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


#create a form
class NamerForm(FlaskForm):
    name = StringField ()


if __name__ == '__main__':
    app.run(debug=True)