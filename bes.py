from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    name ='Welcome'
    return render_template('home.html', name=name )

@app.route('/about')
def about():
    name ='About'
    return render_template('about.html', name=name)

@app.route('/gallery')
def gallery():
    images = ["case.jpeg","klinci/jpeg","loncarstvo.jpg"]
    name ='Photo Gallery'
    return render_template('gallery.html', name=name, images=images)

@app.route('/store')
def shop():
    name='Store'
    return render_template('store.html', name=name)

@app.route('/workshops')
def workshops():
    name='Workshops'
    return render_template('workshops.html',name=name)

@app.route('/proba_galerija')
def proba_galerija():
    images_row = ["zdjela_gline.jpeg","loncarstvo.jpg","klinci.jpg"]
    images_row_1 = ["vaza.jpeg","radione.jpeg","radionica_klinci.jpeg"]
    images_row_2 = ["vaze.jpeg","velika_zdjela.jpeg","case.jpeg"]
    name='Proba Galerija'
    return render_template('proba_galerija.html',name=name, images_row=images_row, images_row_1=images_row_1, images_row_2=images_row_2)

app.run(debug=True)