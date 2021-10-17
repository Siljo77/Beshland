from flask import Flask, render_template
from  flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivansijan:medvescak77@localhost/ivansijan'
# Initialize the database
db = SQLAlchemy(app)


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
