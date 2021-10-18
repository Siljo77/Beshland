from flask import Flask, render_template
from  flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivansijan:medvescak77@localhost/siljo'
# Initialize the database
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    pet = db.Column(db.String(40))

    def __init__(self,first_name,last_name,pet):
        self.first_name=first_name
        self.last_name=last_name
        self.pet=pet
        
    

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
    name = 'LOG IN'
    return render_template('log_in.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
