import sqlite3
from flask import Flask, request, render_template, url_for, redirect


app = Flask(__name__, template_folder='templates', static_folder='static')

basket_cart = list()
# @app.route('/basket')
# def basket():
#     return render_template('basket.html')

@app.route('/frontpage')
def frontpage():
    connect = sqlite3.connect('restaurants.sqlite')
    cursor = connect.cursor()
    cursor.execute("SELECT name, rating, image_url FROM restaurants")
    restaurants = cursor.fetchall()
    connect.close()
    return render_template('frontpage.html', restaurants=restaurants)


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

@app.route('/menu/<restaurant>', methods=['GET'])
def show_menu(restaurant: str):
    conn = sqlite3.connect('restaurants.sqlite')
    cursor = conn.cursor()
    
    cursor.execute("SELECT item_name, description, price, image_url FROM menu WHERE name=?", [restaurant])
    data = cursor.fetchall()
    conn.close()

    if not data:
        # This resturant does not exist
        # TODO: Handle appropriately
        return redirect(url_for('frontpage'))

    # print(data)
    return render_template('menu.html', restaurant_menu=data, restaurant=restaurant)


@app.route('/add-to-basket', methods=['POST','GET'])
def add_to_basket():
    global basket_cart
    if request.method == 'GET':
        return render_template('basket.html',basket_cart_data=basket_cart)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        basket_cart.append({
            'item_name' : form_data.get('item_name'),
            'item_price' : form_data.get('item_price')
        })
        return redirect(url_for('show_menu', restaurant=form_data.get('restaurant_name')))

@app.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    if request.method == 'POST':
        item_index = int(request.form['item_index'])
        del basket_cart[item_index]
        return redirect(url_for('show_basket'))

@app.route('/basket')
def show_basket():
    global basket_cart
    total_price = 0
    for i in basket_cart:
        total_price+=float(i['item_price'].replace('£',''))
    total_price = "{:.2f}".format(total_price)
    return render_template('basket.html', basket_cart_data=basket_cart, total_price=total_price)

@app.route('/checkout',  methods=['POST'])
def checkout_cal():
    global basket_cart
    total_price = 0
    for i in basket_cart:
        total_price+=float(i['item_price'].replace('£',''))

    total_price = "{:.2f}".format(total_price)
    total_price = float(total_price)
    if request.method == 'POST':
        tip = request.form['tip']
        print('check out this tip:',tip,type(tip))
        if tip in ['not_now','10%','15%']:
            if tip == 'not_now':
                tip = 0.0
            elif tip == '10%':
                tip = total_price * 0.10
            elif tip == '15%':
                tip = total_price * 0.10
        else:
            tip = float(tip)

        
        total_price_with_tip = tip + float(total_price)
        total_price_with_tip = "{:.2f}".format(total_price_with_tip)
        return render_template('checkout.html',item_price = total_price, tip = tip, total_price=total_price_with_tip, basket_cart_data=basket_cart)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)