from flask import Flask, render_template, flash, request
from flask.wrappers import Request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

app.config['SECRET_KEY'] = 'medvescak77'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivansijan:medvescak77@localhost/users'
# Initialize the database
db = SQLAlchemy(app)



class users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
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
        
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message= 'Passwords Must Match!')]) 
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])                              
    submit = SubmitField("Submit")        

#@app.route('/update/<int:id>', methods=['GET', 'POST'])
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html", form=form, name_to_update=name_to_update,)
        except:
            db.session.commit()
            flash("Error, try again!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)
           

class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])                   
    submit = SubmitField("Submit")

#@app.route('/user/add', methods=['GET', 'POST'])
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = users(name=form.name.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("User Submmitted Successfully")
        elif user is not None:
            flash("User already has an account")
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash = ''
    
    our_users = users.query.order_by(users.date_added)
    return render_template("add_user.html",form=form,name=name, our_users=our_users)


@app.route('/')
@app.route('/index')
def index():
    name = "Welcome to Beshland"
    return render_template('index.html' , name=name) 


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"), 404
 
@app.errorhandler(500)
def page_not_found(e):
     return render_template("404.html"), 500
 
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submmitted Successfully")
        
    return render_template("name.html", name=name, form=form)

if __name__ == '__main__':
    app.run(debug=True)
