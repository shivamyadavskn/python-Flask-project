from flask import Flask, render_template, request
from flask_mysqldb import MySQL

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


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('uname')
        firstname = request.form.get('fname')
        lastname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        querydata = 'insert into register values(username,email,password,firstname,lastname)'
        insertedData = cur.execute(querydata)
        print('data successfully executed')
        mysql.close()
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/default')
def home():
    cur = mysql.connection.cursor()
    user = cur.execute("select * from register")
    items = cur.fetchall()
    return render_template('home1.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
