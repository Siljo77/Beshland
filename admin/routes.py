from db import db
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, logout_user, login_user,current_user
from admin.forms import UpdateForm, UserForm, LoginForm, ProductsForm
from admin.users import Users
from admin.products import Products
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
    images_row = {'bes_slika.jpeg':'Zastori' + ' -- ' + '335 kn',
                  "bes_slika2.jpeg":'Lampe' + ' -- ' + '500 kn',
                  "bes_slika3.jpeg":'Casa' + ' -- ' + '150 kn',
                  "bes_slika4.jpeg":'Radovi' + ' -- ' + '350 kn',
                  "bes_slika5.jpeg":'Stol' + ' -- ' + '800 kn', 
                  "radionica_klinci.jpeg":"Djeca" + ' -- ' + '300 kn', 
                  "vaze.jpeg":'Vaze' + ' -- ' + '400 kn', 
                  "velika_zdjela.jpeg":'Kolo' + ' -- ' + '250 kn',
                  "case.jpeg":'Sarene case' + ' -- ' + '170 kn'}
    
    images_row_clay = {'bes_slika.jpeg':'Zastori' + ' -- ' + '335 kn',
                  "bes_slika2.jpeg":'Lampe' + ' -- ' + '500 kn',
                  "bes_slika3.jpeg":'Casa' + ' -- ' + '150 kn',
                  "bes_slika4.jpeg":'Radovi' + ' -- ' + '350 kn',
                  "bes_slika5.jpeg":'Stol' + ' -- ' + '800 kn', 
                  "radionica_klinci.jpeg":"Djeca" + ' -- ' + '300 kn', 
                  "vaze.jpeg":'Vaze' + ' -- ' + '400 kn', 
                  "velika_zdjela.jpeg":'Kolo' + ' -- ' + '250 kn',
                  "case.jpeg":'Sarene case' + ' -- ' + '170 kn'}
    
    images_row_workshop = {'bes_slika.jpeg':'Zastori' + ' -- ' + '335 kn',
                  "bes_slika2.jpeg":'Lampe' + ' -- ' + '500 kn',
                  "bes_slika3.jpeg":'Casa' + ' -- ' + '150 kn',
                  "bes_slika4.jpeg":'Radovi' + ' -- ' + '350 kn',
                  "bes_slika5.jpeg":'Stol' + ' -- ' + '800 kn', 
                  "radionica_klinci.jpeg":"Djeca" + ' -- ' + '300 kn', 
                  "vaze.jpeg":'Vaze' + ' -- ' + '400 kn', 
                  "velika_zdjela.jpeg":'Kolo' + ' -- ' + '250 kn',
                  "case.jpeg":'Sarene case' + ' -- ' + '170 kn'}
    
    return render_template('admin/gallery.html', page_name=page_name, images_row=images_row, 
                           images_row_clay=images_row_clay, images_row_workshop = images_row_workshop)


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



#Create Uppdate page
@admin_routes.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']

        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("admin/update.html", form=form,  name_to_update=name_to_update)
        except:
            db.session.commit()
            flash("Error, try again!")
            return render_template("admin/update.html", form=form,  name_to_update=name_to_update)
    else:
        return render_template("admin/update.html", form=form,  name_to_update=name_to_update, id=id)


@admin_routes.route('/delete/<int:id>')
def delete_user(id):
    name = None
    form = UpdateForm()
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully") 
        
        our_users = Users.query.order_by(Users.date_added)
        return render_template("admin/add_user.html", 
        form=form, name=name, 
        our_users=our_users)
    except:
        flash('Sory, there is a problem with deleting this account!')
        return render_template("admin/add_user.html", 
        form=form, name=name, 
        our_users=our_users)
        
        
@admin_routes.route('/products',methods=['GET', 'POST'])
def products():
    page_name = 'Add Product'
    name = None
    form = ProductsForm()
    if form.validate_on_submit():
        user = Products.query.filter_by(name=form.name.data).first()
        if user is None:
            user = Products(name = form.name.data, price=form.price.data, amount=form.amount.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        flash("Product successfully added!")


    return render_template("admin/products.html",form=form, name=name,page_name=page_name)    


#ERROR HANDELER 404
@admin_routes.errorhandler(404)
def page_not_found(e):
    return render_template("public/404.html"), 404


 #ERROR HANDELER 500
@admin_routes.errorhandler(500)
def page_not_found(e):
    return render_template("public/404.html"), 500