from flask import Flask, render_template, request, redirect, url_for, session
from gunicorn app:app import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# بيانات مؤقتة
users = {}  # {اسم المستخدم: كلمة السر}
products = []  # قائمة المنتجات

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        whatsapp = request.form['whatsapp']
        image = request.files['image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        products.append({
            'name': name,
            'price': price,
            'image': filename,
            'owner': session['username'],
            'whatsapp': whatsapp
        })
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
