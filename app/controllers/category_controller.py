from flask import request, jsonify
from http import HTTPStatus

from app.models.categories_model import Category
from app.configs.database import db

from sqlalchemy.exc import IntegrityError





def create_category():
    data = request.get_json()

    data['name'] = data['name'].lower()

    try:
        category = Category(**data)

        db.session.add(category)
        db.session.commit()

        return jsonify(category), HTTPStatus.CREATED

    except IntegrityError:
        return {'error': f'category already exists'}, HTTPStatus.CONFLICT





def update_category(category_id: int):
    data = request.get_json()

    category = Category.query.get(category_id)

    if not category:
        return {'error': 'category not found'}, HTTPStatus.NOT_FOUND

    try:
        if 'name' in data:
            data['name'] = data['name'].lower()
            setattr(category, 'name', data['name'])
            

        if 'description' in data:
            setattr(category, 'description', data['description'])
            

        db.session.add(category)
        db.session.commit()

        return jsonify(category), HTTPStatus.OK

    except IntegrityError:
        return {'error': f'category already exists'}, HTTPStatus.CONFLICT




def remove_category(category_id: int):

    category = Category.query.get(category_id)

    if not category:
        return {'error': 'category not found'}, HTTPStatus.NOT_FOUND
    

    db.session.delete(category)
    db.session.commit()

    return '', HTTPStatus.NO_CONTENT




