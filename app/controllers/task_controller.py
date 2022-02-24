from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.tasks_model import Task
from app.models.eisenhowers_model import Eisenhower
from app.models.categories_model import Category
from app.configs.database import db

from app.exc.tasks_exc import ValidadeImportanceUrgency



def create_task():
    data = request.get_json()
    session: Session = db.session
    base_query = session.query(Eisenhower)

    categories = data.pop('categories')

    data['name'] = data['name'].lower()

    try: 
        if data['importance'] == 1 and data['urgency'] == 1:
            type_filter = base_query.filter(Eisenhower.type_eisenhower == 'Do It First').first()
            data['eisenhowers_id'] = type_filter.id_eisenhower

        if data['importance'] == 1 and data['urgency'] == 2:
            type_filter = base_query.filter(Eisenhower.type_eisenhower == 'Delegate It').first()
            data['eisenhowers_id'] = type_filter.id_eisenhower

        if data['importance'] == 2 and data['urgency'] == 1:
            type_filter = base_query.filter(Eisenhower.type_eisenhower == 'Schedule It').first()
            data['eisenhowers_id'] = type_filter.id_eisenhower

        if data['importance'] == 2 and data['urgency'] == 2:
            type_filter = base_query.filter(Eisenhower.type_eisenhower == 'Delete It').first()
            data['eisenhowers_id'] = type_filter.id_eisenhower

    
        task = Task(**data)


        for category_not_exist in categories:
            category_filter = Category.query.filter(Category.name == category_not_exist.lower()).first()
            if not category_filter:
                new_category = Category(name=category_not_exist.lower())
                db.session.add(new_category)
                db.session.commit()


        category_list= []

        for category in categories:
            category_filter = Category.query.filter(Category.name == category.lower()).first()
            if category_filter:
                 category_list.append(category.lower())
        
        

        classification = base_query.filter(Eisenhower.id_eisenhower == task.eisenhowers_id).first().type_eisenhower

        db.session.add(task)
        db.session.commit()

        return {
            'id_task': task.id_task,
            'name': task.name,
            'description': task.description,
            'duration': task.duration,
            'classification': classification,
            'categories': category_list
        }, HTTPStatus.CREATED
       

    except ValidadeImportanceUrgency:
        return {
            "msg": {
                "valid_options": {
                    "importance": [1, 2], 
                    "urgency": [1, 2]
                },
                "recieved_options": {
                    "importance": data['importance'],
                    "urgency": data['urgency']
                }
            }
        }, HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {'error': f'task already exists'}, HTTPStatus.CONFLICT       





def update_task(task_id: int):
    data = request.get_json()
    session: Session = db.session
    base_query = session.query(Eisenhower)


    task = Task.query.get(task_id)
    

    if not task:
        return {'error': 'task not found'}, HTTPStatus.NOT_FOUND

    
    try:
        if 'name' in data:
            data['name'] = data['name'].lower()
            setattr(task, 'name', data['name'])
    
        if 'description' in data:
            setattr(task, 'description', data['description'])

        if 'duration' in data:
            setattr(task, 'duration', data['duration'])

        if 'importance' in data:
            setattr(task, 'importance', data['importance'])

        if 'urgency' in data:
            setattr(task, 'urgency', data['urgency'])



        db.session.add(task)
        db.session.commit()

        return jsonify(task), HTTPStatus.CREATED


    except ValidadeImportanceUrgency:
        return {
            "msg": {
                "valid_options": {
                    "importance": [1, 2], 
                    "urgency": [1, 2]
                },
                "recieved_options": {
                    "importance": data['importance'],
                    "urgency": data['urgency']
                }
            }
        }, HTTPStatus.BAD_REQUEST

    except IntegrityError:
        return {'error': f'task already exists'}, HTTPStatus.CONFLICT

    





def remove_task(task_id: int):

    task = Task.query.get(task_id)

    if not task:
        return {'error': 'task not found'}, HTTPStatus.NOT_FOUND
    

    db.session.delete(task)
    db.session.commit()

    return '', HTTPStatus.NO_CONTENT


