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
    images = ["case.jpeg","klinci.jpg","loncarstvo.jpg","puno_casa.jpeg","radione.jpeg","radionica_klinci.jpeg","vaza.jpeg","vaze.jpeg","velika_zdjela.jpeg","zdjela_gline.jpeg"]
    name='Proba_Galerija'
    return render_template('proba_galerija.html',name=name, images=images)

app.run(debug=True, port=5009)