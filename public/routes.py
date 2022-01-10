from db import db
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, logout_user, login_user,current_user
from public.forms import UserForm, LoginForm, UpdateForm, ProductsForm
from admin.users import Users
from admin.products import Products
from werkzeug.security import generate_password_hash


public_routes = Blueprint('public_routes', __name__, static_folder="static", template_folder="templates")


#Create Index Page
@public_routes.route('/index')
@public_routes.route('/')
def index():
    page_name = "Index"
    name = "Welcome to Beshland"
    return render_template('public/index.html', name=name, page_name=page_name)


#Create About Page
@public_routes.route('/about')
def about():
    page_name = 'About'
    return render_template('public/about.html', page_name=page_name)


#Create Gallery Page
#Create Gallery Page
@public_routes.route('/explore')
def explore():
    page_name = 'Explore'
    images_webshop = "static/img/bes_slika1.jpeg"
    images_workshop = "static/img/bes_slika3.jpeg"
    images_gallery =  "static/img/bes_slika4.jpeg"
    
    return render_template('public/explore.html', page_name=page_name, images_webshop=images_webshop,
                           images_gallery=images_gallery, images_workshop=images_workshop)

#Create Dashboard page
@public_routes.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    page_name = "Dashboard"
    return render_template("public/dashboard.html", page_name=page_name)


#Create Logout Page
@public_routes.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You Have Been Logged Out!')
    return redirect(url_for('public_routes.login'))


#Create Loign page
@public_routes.route('/login', methods=['GET', 'POST'])
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
                return redirect(next or url_for('public_routes.dashboard'))
            else:
                flash('Wrong Password -- Try Again!')
        else:
            flash("That User Dosn't Exist! Try Again")
    return render_template("public/login.html", page_name=page_name, form=form)



#Create and Add User Page
@public_routes.route('/user/add', methods=['GET', 'POST'])
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
    return render_template("public/add_user.html", page_name=page_name, form=form, name=name, our_users=our_users)



#Create Uppdate page
@public_routes.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UpdateForm()
    name_to_update = Users.query.get_or_404(id)
    if form.validate_on_submit():
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
    
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("public/dashboard.html", form=form,  name_to_update=name_to_update)
        except:
            flash("Failed")
            return render_template("public/update.html", form=form,  name_to_update=name_to_update)
        
    return render_template("public/update.html", form=form,  name_to_update=name_to_update, id=id)


@public_routes.route('/gallery')
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

    return render_template('public/gallery.html', page_name=page_name, images_row=images_row)


@public_routes.route('/products',methods=['GET', 'POST'])
def products():
    page_name = 'Add Product'
    name = None
    form = ProductsForm()
    if form.validate_on_submit():
        product = Products.query.filter_by(name=form.name.data).first()
        if product is None:
            product = Products(name = form.name.data, price=form.price.data, amount=form.amount.data)
            db.session.add(product)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        flash("Product successfully added!")


    return render_template("public/products.html",form=form, name=name,page_name=page_name) 


@public_routes.route('/update_product/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):
    form = ProductsForm()
    amount_to_update = Products.query.get_or_404(id)
    if request.method == "POST":
        amount_to_update.amount = request.form['amount']
        
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("public/update_product.html", form=form,  amount_to_update=amount_to_update)
        except:
            db.session.commit()
            flash("Error, try again!")
            return render_template("public/update_product.html", form=form,  amount_to_update=amount_to_update)
        
    else:
        return render_template("public/update_product.html", form=form, amount_to_update=amount_to_update, id=id)


@public_routes.route('/webshop')
def webshop():
    page_name = "Webshop"
    return render_template('public/webshop.html', page_name=page_name)


@public_routes.route('/workshop')
def workshop():
    page_name = 'Workshop'
    return render_template('public/workshop.html', page_name=page_name)


@public_routes.route('/addresses')
def addresses():
    page_name = 'My Account'
    return render_template("/public/addresses.html", page_name=page_name)


@public_routes.route('/cups')
def cups():
    page_name = "Cups"
    images = ["bes_casa_1.jpeg","bes_casa_2.jpeg","bes_casa_3.jpeg",
              "bes_casa_4.jpeg","bes_casa_3.jpeg","bes_casa_3.jpeg"]
    return render_template('public/cups.html', page_name=page_name,images=images)


@public_routes.route('/chandeliers')
def chandeliers():
    page_name = "Chandeliers"
    return render_template('public/chandeliers.html', page_name=page_name)


@public_routes.route('/sets')
def sets():
    page_name = "Sets"
    images_row = ["komplet_casa_1.jpeg",
                  "komplet_casa_2.jpeg",
                  "komplet_casa_3.jpeg",
                  "komplet_casa_4.jpeg",
                  "komplet_casa_5.jpeg",
                  "komplet_casa_3.jpeg"]
    
    return render_template('public/sets.html', page_name=page_name, images_row=images_row)


@public_routes.route('/casa_size')
def casa_size():
    page_name = ""
    return render_template('public/casa_size.html', page_name=page_name)
    
    
@public_routes.route('/cart')
def cart():
    page_name = "Your Cart"
    return render_template('public/cart.html', page_name=page_name)
                           


#ERROR HANDELER 404
@public_routes.errorhandler(404)
def page_not_found(e):
    return render_template("public/404.html"), 404


 #ERROR HANDELER 500
@public_routes.errorhandler(500)
def page_not_found(e):
    return render_template("public/404.html"), 500


