from db import DB
import datetime
from flask import Flask, jsonify, render_template, url_for, request, redirect, flash, request
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import settings


app = Flask(__name__)
app.secret_key = 'secret'
login_manager = LoginManager(app)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{settings.USER}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app_root = os.path.dirname(os.path.abspath(__file__))

# DB Model USER for auth
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDataBase(user_id, User)


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    """Авторизация"""
    if request.method == "POST":
        user_data = DB().get_user(request.form['login'])[0]

        if user_data[2] == request.form['password'] and user_data[1] == request.form['login']:
            user_login = UserLogin().create(user_data)
            login_user(user_login)

            return redirect(url_for('index'))
        # flash('Ошибка')
    return render_template('auth.html')

@app.route('/products', methods=['POST', 'GET'])
@login_required
def products():
    """Товары страница"""

    data = DB().get_all_goods()
    ids = [i[0] for i in data]
    print(data)
    if request.method == "POST":

        id_ = request.form['id']
        title = request.form['title']
        manufacturer = request.form['manufacturer']
        # save img
        if request.files['img'].content_type != 'application/octet-stream':
            img = request.files['img'].filename
            destination = '/'.join([settings.IMG_PATH, img])
            request.files['img'].save(destination)
        else:
            img = None

        information = request.form['information']
        price = request.form['price']
        leave_condition = request.form['leave_condition']

        if id_ not in ids:
            DB().add_goods({'id': id_, 'title': title, 'manufacturer': manufacturer, 'img': img,
                            'information': information, 'price': price, 'leave_condition': leave_condition})
        else:
            DB().update_goods(
                {'id': id_, 'title': title, 'manufacturer': manufacturer, 'img': img,
                            'information': information, 'price': price, 'leave_condition': leave_condition})

        return redirect(url_for('products'))

    # Возвращает html Товары страницы
    return render_template('index.html', data=data)


@app.route('/pharmacies', methods=['POST', 'GET'])
@login_required
def pharmacies():
    """Страница с аптеками"""

    data = DB().get_all_pharmacy()
    ids = [i[0] for i in data]

    # Добавление новой позиции
    if request.method == "POST":

        id_ = int(request.form['id'])
        title = request.form['title']
        address = request.form['address']
        phone = request.form['phone']
        schedule = request.form['schedule']
        if id_ not in ids:
            DB().add_pharmacy(
                {'id': int(id_), 'title': title, 'address': address, 'phone': phone, 'schedule': schedule})
        else:
            DB().update_pharmacy(
                {'id': int(id_), 'title': title, 'address': address, 'phone': phone, 'schedule': schedule})
        return redirect(url_for('pharmacies'))

    # Возвращает pharmacies
    return render_template('pharmacies.html', data=data)

@app.route('/available', methods=['POST', 'GET'])
@login_required
def available():
    """Страница с наличием"""

    data = DB().get_all_available()
    ids = [i[0] for i in data]

    # Добавление новой позиции
    if request.method == "POST":

        id_pharmacy = int(request.form['id_pharmacy'])
        id_good = request.form['id_good']
        available = request.form['available']
        if id_pharmacy not in ids:
            DB().add_available(
                {'id_pharmacy': int(id_pharmacy), 'id_good': id_good, 'available': available})
        else:
            DB().update_available(
                {'id_pharmacy': int(id_pharmacy), 'id_good': id_good, 'available': available})
        return redirect(url_for('available'))

    # Возвращает pharmacies
    return render_template('available.html', data=data)

@app.route('/available/<string:id>', methods=['POST', 'GET'])
@login_required
def available_get(id):
    data=DB().get_pharmacy_available_by_id(id)
    print(data)
    data = [[i[-3], i[-2], i[-1]] for i in data]
    print(data)
    return render_template('available.html', data=data)

@app.route('/')
@login_required
def index():
    return render_template('home.html')

@app.route('/reviews/<string:id>')
@login_required
def reviews(id):

    data = DB().get_reviews_by_id(id)
    print(data)
    return render_template('reviews.html', data=data)

@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    if request.method == "POST":

        text = request.form['text']
        data = DB().get_good_by_title(text)
        if len(data) == 0:
            data = DB().get_good_by_id(text)
            if len(data) == 0:
                data = []
    

    return render_template('search.html', data=data)


@app.route('/del/<string:id>')
@login_required
def delete(id):
    try:
        DB().delete_reviews(id)
    except Exception as e:
        pass

    try:
        DB().delete_available(id)
    except Exception as e:
        pass

    try:
        DB().delete_good(id)
    except Exception as e:
       pass

    data = DB().get_all_goods()
    return render_template('index.html', data=data)


if __name__ == "__main__":
    # Запуск
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=False)
