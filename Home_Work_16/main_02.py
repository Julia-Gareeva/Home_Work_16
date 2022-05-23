from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from data_01 import users, orders, offers
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(75))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(80))
    phone = db.Column(db.String(50))


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(350))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))


db.create_all()

#######################################################################################################################
def insert_data_01():
    user_list = []
    for user in users:
        user_list.append(
            User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone'],
            )
        )
        with db.session.begin():
            db.session.add_all(user_list)

    order_list = []
    for order in orders:
        order_list.append(
            Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
                end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id'],
            )
        )
        with db.session.begin():
            db.session.add_all(order_list)

    offer_list = []
    for offer in offers:
        order_list.append(
            Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id'],
            )
        )
        with db.session.begin():
            db.session.add_all(offer_list)

##############################################################################################################


@app.route('/', methods=['GET', 'POST'])
def get_users_01():

    # Создать представления по методу 'GET' для /users.
    if request.method == 'GET':
        data = []
        for user in User.query.all():
            data.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'email': user.email,
                'role': user.role,
                'phone': user.phone,
            })
        return jsonify(data)
    # Создать представления по методу 'GET' для /users/1 для получения одного пользователя.
    elif request.method == 'GET':
            user = User.query.get(id)
            data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'email': user.email,
                'role': user.role,
                'phone': user.phone,
            }
            return jsonify(data)
    # Посредством метода 'POST' на URL /users реализовать создание пользователя.
    elif request.method == 'POST':
        data = request.get_json()
        new_users = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            email=data['email'],
            role=data['role'],
            phone=data['phone'],
        )
        db.session.add(new_users)
        db.session.commit()
    else: "Ошибка."


@app.route('/users/', methods=['PUT', 'DELETE'])
def get_users_02():
    # Посредством метода 'PUT' на URL /users/<id> реализовать обновление пользователя user.
    if request.method == 'PUT':
        data = request.get_json()
        user = User.query.get(id)
        user.first_name = 'new_user'
        user.last_name = data['last_name']
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']

        db.session.add(user)
        db.session.commit()
        return '', 203
    # Посредством метода 'DELETE' на URL /users/<id> реализовать удаление пользователя user.
    elif request.method == 'DELETE':
        user = Order.query.get(id)
        db.session.add(user)
        db.session.commit()
    else: "Ошибка."

#######################################################################################################

# Создать представления по методу 'GET' для /orders
@app.route('/orders/')
def get_orders():
    pass


# Создать представления по методу 'GET' для /orders/1 для получения одного пользователя
@app.route('/orders/<int:id>/')
def get_orders_by_id(id):
    pass


# Посредством метода 'POST' на URL /orders реализовать создание пользователя
@app.route('/orders/post/')
def orders_post():
    pass


# Посредством метода 'PUT' на URL /orders/<id> реализовать обновление заказа order
@app.route('/orders/<int:id>/put/')
def orders_put():
    pass


# Посредством метода 'DELETE' на URL /orders/<id> реализовать удаление заказа order
@app.route('/orders/<int:id>/delete/')
def orders_delete():
    pass


#######################################################################################################################

# Создать представления по методу 'GET' для /offers
@app.route('/offers/')
def get_offers():
    pass


# Создать представления по методу 'GET' для /offers/<id> для получения одного пользователя
@app.route('/offers/<int:id>/')
def get_offers_by_id(id):
    pass


# Посредством метода 'POST' на URL /offers реализовать создание пользователя
@app.route('/offers/post/')
def offers_post():
    pass


# Посредством метода 'PUT' на URL /offers/<id> реализовать обновление предложения offer
@app.route('/offers/<int:id>/put/')
def offers_put():
    pass


# Посредством метода 'DELETE' на URL /offers/<id> реализовать удаление предложения offer
@app.route('/offers/<int:id>/delete/')
def offers_delete():
    pass


def main():
    insert_data_01()

    app.run(debug=True)


if __name__ == "__main__":
    main()