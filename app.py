from os import error
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivansijan:medvescak77@localhost/login'
# Initialize the database
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__="Login"
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(40))
    password = db.Column(db.String(40))

    def __init__(self,email,password):
         self.email=email
         self.password=password
    
        
@app.route('/')
@app.route('/index')
def home():
    name = 'Welcome'
    return render_template('index.html', name=name)


@app.route('/about')
def about():
    name = 'About'
    return render_template('about.html', name=name)


@app.route('/gallery')
def gallery():
    images_row = ["zdjela_gline.jpeg", "loncarstvo.jpg", "klinci.jpg"]
    images_row_1 = ["vaza.jpeg", "radione.jpeg", "radionica_klinci.jpeg"]
    images_row_2 = ["vaze.jpeg", "velika_zdjela.jpeg", "case.jpeg"]
    name = 'Photo Gallery'
    return render_template('gallery.html', name=name, images_row=images_row, images_row_1=images_row_1, images_row_2=images_row_2)


@app.route('/webshop')
def webshop():
    name = 'Webshop'
    return render_template('webshop.html', name=name)


@app.route('/workshops')
def workshops():
    name = 'Workshops'
    return render_template('workshops.html', name=name)

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    name = "Log in"
    return render_template('log_in.html', name=name)

@app.route('/fail', methods=['GET', 'POST'])
def fail():
    name = "fail"
    return render_template('fail.html', name=name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    name = "Create new account"
    return render_template('register.html', name=name)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']


        if not email or not password :
            error_statement = "All Form Fileds Required"
            return render_template("fail.html",email=email, password=password,error_statement=error_statement)


        user = User(email, password)
        db.session.add(user)
        db.session.commit()
        

    return render_template('success.html')
 

if __name__ == '__main__':
    app.run(debug=True)
        


