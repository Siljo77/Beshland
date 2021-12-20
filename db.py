from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def initDb(app):
    app.config['SECRET_KEY'] = 'medvescak77'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivansijan:medvescak77@localhost/users'
    db.init_app(app)

