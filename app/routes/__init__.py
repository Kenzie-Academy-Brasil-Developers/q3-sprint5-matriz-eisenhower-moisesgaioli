from flask import Flask, Blueprint
from app.routes.category_route import bp as bp_categories
from app.routes.task_route import bp as bp_tasks



bp_api = Blueprint('api', __name__, url_prefix='/api')

def init_app(app: Flask):
    
    bp_api.register_blueprint(bp_tasks)
    bp_api.register_blueprint(bp_categories)

    app.register_blueprint(bp_api)