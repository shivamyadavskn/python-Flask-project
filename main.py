from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "1234"
app.config['MYSQL_DB'] = "alchemy"
mysql = MySQL(app)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('uname')
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO register values(%s,%s,%s,%s,%s)", (username, email, password, firstname, lastname))
        mysql.connection.commit()
        cur.close()
        print('data successfully executed')
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/default')
def home():
    cur = mysql.connection.cursor()
    cur.execute("select * from register")
    items = cur.fetchall()
    return render_template('home1.html', items=items)


@app.route('/dummy', methods=['GET', 'POST'], )
def dummy():
    print('email' in request.form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        print('email' in request.form)
        email = request.form['email']
        print(email)
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT*FROM dummy where email=%s", (email,))
        account = cur.fetchone()
        print(account)
        if account:
            msg = 'Account already exists'
            print(msg)
        elif not email or not password:
            msg = 'Fill out form'
            print(msg)
        else:
            cur.execute("INSERT INTO dummy values(%s,%s)", (email, password))
            mysql.connection.commit()
            cur.close()
            print("Successfully Inserted Data")
    else:
        return render_template('dummy.html')


if __name__ == '__main__':
    app.run(debug=True)
