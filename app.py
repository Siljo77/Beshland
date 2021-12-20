import os
from flask import Flask
from db import initDb, db


template_dir = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_dir)


initDb(app)

from admin.products import Products, Products2
with app.app_context():
    db.create_all()


from public.routes import public_routes, index as public_index
from admin.routes import admin_routes
from admin.login_manager import login_manager, startLogin
from admin.users import Users

app.register_blueprint(public_routes, url_prefix="/public")
app.register_blueprint(admin_routes, url_prefix="/admin")
startLogin(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    return public_index()

if __name__ == '__main__':
    app.run(debug=True)
