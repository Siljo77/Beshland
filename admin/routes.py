from db import db
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, logout_user, login_user,current_user
from admin.forms import UserForm, LoginForm
from admin.users import Users
from werkzeug.security import generate_password_hash


admin_routes = Blueprint('admin_routes', __name__, static_folder="static", template_folder="templates")


@admin_routes.route('/loginrequired', methods=['GET', 'POST'])
@login_required
def loginrequired():
    return render_template("admin/dashboard.html", page_name='login')


#Create Index Page
@admin_routes.route('/index')
@admin_routes.route('/')
@login_required
def index():
    page_name = "Index"
    name = "Welcome to Beshland"
    return render_template('admin/index.html', name=name, page_name=page_name)


#Create About Page
@admin_routes.route('/about')
@login_required
def about():
    page_name = 'About'
    return render_template('admin/about.html', page_name=page_name)
    


#Create Gallery Page
@admin_routes.route('/gallery')
@login_required
def gallery():
    page_name = 'Gallery'
    images_row = ["zdjela_gline.jpeg", "loncarstvo.jpg", "klinci.jpg", "vaza.jpeg",
                  "radione.jpeg", "radionica_klinci.jpeg", "vaze.jpeg", "velika_zdjela.jpeg", "case.jpeg"]
    return render_template('admin/gallery.html', page_name=page_name, images_row=images_row)


#Create Dashboard page
@admin_routes.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    page_name = "Dashboard"
    return render_template("admin/dashboard.html", page_name=page_name)


#Create Logout Page
@admin_routes.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You Have Been Logged Out!')
    return redirect(url_for('admin_routes.login'))

#Create Loign page
@admin_routes.route('/login', methods=['GET', 'POST'])
def login():
    page_name = "Login"
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if user.verify_password(password=form.password.data):
                login_user(user)
                flash('Login Successfull')
                next = request.args.get('next')
                return redirect(next or url_for('admin_routes.dashboard'))
            else:
                flash('Wrong Password -- Try Again!')
        else:
            flash("That User Dosn't Exist! Try")
    return render_template("admin/login.html", page_name=page_name, form=form)


#Create and Add User Page
@admin_routes.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    page_name = "Create Account"
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(
                form.password_hash.data, "sha256")
            user = Users(name=form.name.data, username=form.username.data,
                         email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("User Submmitted Successfully")
        elif user is not None:
            flash("Already has an account")
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.password_hash = ''

    our_users = Users.query.order_by(Users.date_added)
    return render_template("admin/add_user.html", page_name=page_name, form=form, name=name, our_users=our_users)




def out(updatePage, error, name_to_update):
    return render_template(updatePage, form=UserForm(), name_to_update=name_to_update, error=error)


def wrapReturnMsg(type, error):
    return {
        "type": type,
        "error": error
    }


def _error(updatePage, error, name_to_update):
    return out(updatePage, wrapReturnMsg("error", error), name_to_update)


def _warning(updatePage, error, name_to_update):
    return out(updatePage,  wrapReturnMsg("warning", error), name_to_update)


def _info(updatePage, error, name_to_update):
    return out(updatePage, wrapReturnMsg("info", error), name_to_update)

#Create Uppdate page
@admin_routes.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):

    updatePage = 'admin/update.html'

    def error(error):
        return _error(updatePage, error, False)

    def info(name_to_update, error=False):
        return _info(updatePage, error, name_to_update)

    if int(id) <= 0 or int(id) != current_user.id:
        return error("You do not have access to that user")

    if not request.method == 'POST':
        if request.method == 'GET':
            name_to_update = Users.query.filter_by(id=id).first()
            if not name_to_update:
                return error("nema usera u bazi")
            return info(name_to_update=name_to_update)

    if not request.form['name']:
        return error("nema imena")

    name_to_update = Users.query.filter_by(id=id).first()
    if not name_to_update:
        return error("nema usera u bazi")

    name_to_update.name = request.form['name']
    name_to_update.email = request.form['email']
    name_to_update.username = request.form['username']
    try:
        db.session.commit()
        return info(name_to_update, "User Updated Successfully")
    except:
        db.session.commit()
        return error("Error, try again!", name_to_update)
    

    
#ERROR HANDELER 404
@admin_routes.errorhandler(404)
def page_not_found(e):
    return render_template("public/404.html"), 404


 #ERROR HANDELER 500
@admin_routes.errorhandler(500)
def page_not_found(e):
    return render_template("public/404.html"), 500