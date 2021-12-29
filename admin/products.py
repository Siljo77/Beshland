from db import db
from flask_login import UserMixin

class Products(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
    

