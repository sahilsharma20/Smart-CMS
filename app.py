from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Mock menu
menu_items = [
    {'id': 1, 'name': 'Veg Sandwich', 'price': 40},
    {'id': 2, 'name': 'Masala Dosa', 'price': 50},
    {'id': 3, 'name': 'Cold Coffee', 'price': 30},
]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        college_id = request.form['college_id']
        password = request.form['password']
        if password == 'Admin@12345':
            session['user'] = college_id
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid password.'
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/menu')
def menu():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html', menu=menu_items)

@app.route('/order', methods=['POST'])
def order():
    item_id = request.form['item_id']
    socketio.emit('order_status_update', {'order_id': item_id, 'status': 'Order placed'})
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
