from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ImageCategorisations(db.Model):
    __tablename__ = "image_categorisation"
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(11))
    url = db.Column(db.String())
    username = db.Column(db.String())
    date = db.Column(db.String(8))
    version = db.Column(db.Integer)
    tag = db.Column(db.String())
    strength = db.Column(db.Float)

    def __init__(self, hash, url, username, date, version, tag, strength):
        self.hash = hash
        self.url = url
        self.username = username
        self.date = date
        self.version = version
        self.tag = tag
        self.strength = strength

@app.route('/')
def home():
    return render_template('home.html')
