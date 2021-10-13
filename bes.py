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
    name ='Photo Gallery'
    return render_template('gallery.html', name=name)

@app.route('/store')
def shop():
    name='Store'
    return render_template('store.html', name=name)

@app.route('/workshops')
def workshops():
    name='Workshops'
    return render_template('workshops.html',name=name)

app.run(debug=True)