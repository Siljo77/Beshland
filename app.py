import os
from flask import Flask
from public.routes import public_routes
from admin.routes import admin_routes
from admin.login_manager import login_manager, startLogin
from admin.users import Users
from db import initDb
from public.routes import index as public_index

template_dir = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_dir)

app.register_blueprint(public_routes, url_prefix="/public")
app.register_blueprint(admin_routes, url_prefix="/admin")
startLogin(app)
initDb(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def index():
    return public_index()

if __name__ == '__main__':
    app.run(debug=True)
