from flask import Flask, render_template
from  flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
# Initialize the database
db = SQLAlchemy(app)

#Create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    data_created = db.Columne(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):  
        return '<Name %r>' % self.id


subscribes = []

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


app.run(debug=True)
