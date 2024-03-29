import sqlite3
from flask import Flask, request, render_template, url_for, redirect


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/basket')
def basket():
    return render_template('basket.html')

@app.route('/frontpage')
def frontpage():
    return render_template('frontpage.html')

@app.route("/")
def index():
    return render_template('index.html') 

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        newpassword = request.form['newpassword']
        name = request.form['name']
        dob = request.form['dob']
        address = request.form['address']
        postcode = request.form['postcode']
        phone_number = request.form['phone_number']

        if password != newpassword:
            error = "Passwords do not match"
        else:
            conn = sqlite3.connect('account.sqlite')
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO users (username, password, name, date, address,
            postcode, phonenumber) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, password, name, dob, address, postcode, phone_number))
            conn.commit()
            conn.close()
            return render_template('login.html')

    return render_template('register.html', error=error)

@app.route('/show-register', methods=['GET'])
def show_register():
    return render_template('register.html')


@app.route('/show-login', methods=['GET'])
def show_login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('account.sqlite')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect(url_for('frontpage'))
        else:
            error =  'Invalid username or password'


    return render_template('login.html', error=error)

@app.route('/menu', methods=['GET'])
def show_menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=4000, debug=True)
