from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager
from public.routes import public_routes
from admin.routes import admin_routes
from admin.users import Users

app = Flask(__name__)
app.register_blueprint(public_routes, url_prefix="/public")
app.register_blueprint(admin_routes, url_prefix="/admin")



app.config['SECRET_KEY'] = 'medvescak77'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivansijan:medvescak77@localhost/users'
# Initialize the database
db = SQLAlchemy(app)


# Flask_Login staff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/admin/login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



if __name__ == '__main__':
    app.run(debug=True)
