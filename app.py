from flask import Flask, render_template
from  flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivansijan:medvescak77@localhost/siljo'
# Initialize the database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    
    def __init__(self,username,email):
        self.username = username
        self.email = email
        
    def __repr__(self):
        return "<User %r>" % self.username
    

@app.route('/')
@app.route('/home')
def home():
    name = 'Welcome'
    return render_template('home.html', name=name)


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


@app.route('/store')
def shop():
    name = 'Store'
    return render_template('store.html', name=name)


@app.route('/workshops')
def workshops():
    name = 'Workshops'
    return render_template('workshops.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
