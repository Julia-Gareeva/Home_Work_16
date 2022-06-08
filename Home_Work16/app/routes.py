from app import models, db
from flask import current_app as app, jsonify


@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.query(models.User).all()

    return {}