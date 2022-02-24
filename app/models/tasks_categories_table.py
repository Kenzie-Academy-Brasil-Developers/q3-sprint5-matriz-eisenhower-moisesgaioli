from app.configs.database import db



tasks_categories = db.Table('tasks_categories',
    db.Column('id_task_category', db.Integer, primary_key=True),

    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id_task')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id_category'))
)