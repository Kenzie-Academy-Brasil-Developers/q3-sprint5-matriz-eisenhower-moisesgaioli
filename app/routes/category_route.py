from click import BadParameter
from flask import Blueprint
from app.controllers import category_controller


bp = Blueprint('categories', __name__, url_prefix='/categories')


bp.post('')(category_controller.create_category)
bp.patch('/<int:category_id>')(category_controller.update_category)
bp.delete('/<int:category_id>')(category_controller.remove_category)
