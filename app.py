from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from forms import UserForm, LoginForm

app = Flask(__name__)


app.config['SECRET_KEY'] = 'medvescak77'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivansijan:medvescak77@localhost/users'
# Initialize the database
db = SQLAlchemy(app)


# Flask_Login staff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True )
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(100))
    
                              
    @property
    def password(self):
        raise AttributeError('password is not a redable attribute') 
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)                  
                              
    def __repr__(self):
        return '<Name %r>' % self.name
    

#Create Index Page
@app.route('/')
@app.route('/index')
def index():
    name = "Welcome to Beshland"
    return render_template('index.html' , name=name)


#Create About Page
@app.route('/about')
def about():
    name = 'About'
    return render_template('about.html', name=name)


#Create Gallery Page
@app.route('/gallery')
def gallery():
    images_row = ["zdjela_gline.jpeg", "loncarstvo.jpg", "klinci.jpg", "vaza.jpeg", "radione.jpeg", "radionica_klinci.jpeg", "vaze.jpeg", "velika_zdjela.jpeg", "case.jpeg"]
    images_row_1 = ["vaza.jpeg", "radione.jpeg", "radionica_klinci.jpeg"]
    images_row_2 = ["vaze.jpeg", "velika_zdjela.jpeg", "case.jpeg"]
    return render_template('gallery.html', images_row=images_row, images_row_1=images_row_1, images_row_2=images_row_2)
    
    
#Create and Add User Page
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users( name=form.name.data, username=form.username.data, email=form.email.data, password_hash=hashed_pw)
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
    return render_template("add_user.html",form=form,name=name, our_users=our_users)

   
#Create Loign page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check the hash
            if user.verify_password(password=form.password.data):
                login_user(user)
                flash('Login Successfull')
                next = request.args.get('next')
                return redirect(next or url_for('dashboard'))
            else:
                flash('Wrong Password -- Try Again!')
        else:
            flash("That User Dosn't Exist! Try")
    return render_template("login.html", form=form)


#Create Dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")


#Create Uppdate page
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html", form=form, name_to_update=name_to_update,)
        except:
            db.session.commit()
            flash("Error, try again!")
            return render_template("update.html", form=form, name_to_update=name_to_update,id=id)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update,id=id)


#Create Logout Page
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You Have Been Logged Out!')
    return redirect(url_for('login'))


#ERROR HANDELER 404
@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"), 404
 
 
 #ERROR HANDELER 500
@app.errorhandler(500)
def page_not_found(e):
     return render_template("404.html"), 500
 

if __name__ == '__main__':
    app.run(debug=True)
