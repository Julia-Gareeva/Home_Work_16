from app import models, db
from flask import current_app as app, jsonify, abort


@app.route('/users', methods=['GET'])
def get_users():
    """Возвращает список пользователей."""
    users = db.session.query(models.User).all()

    return jsonify([user.serialize() for user in users])


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Возвращает пользователей по ID."""
    user = db.session.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        abort(404)
    return jsonify(user.serialize())

###_____________________________________________________________________________________________________


@app.route('/orders', methods=['GET'])
def get_orders():
    """Возвращает список заказов."""
    orders = db.session.query(models.Order).all()

    return jsonify([order.serialize() for order in orders])


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Возвращает заказы по ID."""
    order = db.session.query(models.Order).filter(models.Order.id == order_id).first()

    if order is None:
        abort(404)
    return jsonify(order.serialize())

###______________________________________________________________________________________________________


@app.route('/offers', methods=['GET'])
def get_offers():
    """Возвращает список предложений."""
    offers = db.session.query(models.Offer).all()

    return jsonify([offer.serialize() for offer in offers])


@app.route('/offers/<int:offer_id>', methods=['GET'])
def get_offer(offer_id):
    """Возвращает предложения по ID."""
    offer = db.session.query(models.Offer).filter(models.Offer.id == offer_id).first()

    if offer is None:
        abort(404)
    return jsonify(offer.serialize())
