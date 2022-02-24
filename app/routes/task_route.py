from flask import Blueprint
from app.controllers import task_controller


bp = Blueprint('tasks', __name__, url_prefix='/tasks')


bp.post('')(task_controller.create_task)
bp.patch('/<int:task_id>')(task_controller.update_task)
bp.delete('/<int:task_id>')(task_controller.remove_task)
