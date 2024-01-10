from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        dob = request.form['dob']
        address = request.form['address']
        postcode = request.form['postcode']
        phone_number = request.form['phone_number']
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO users (username, password, name, dob, address,
        postcode, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, password, name, dob, address, postcode, phone_number))
        conn.commit()
        conn.close()
        return render_template ('{{ url_for "login"}}')

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('account.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return 'Login successful'
        else:
            return 'Invalid username or password'

    return render_template ('login.html')

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)