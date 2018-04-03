import logging

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

import categories

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/images_analysed'
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
    return render_template('home.html', categories=categories.subject_categories)

@app.route('/<category>')
def category(category):
    if category in categories.subject_categories.keys():        
        images = ImageCategorisations.query.filter(ImageCategorisations.tag == category).filter(ImageCategorisations.strength > 0.2).order_by(ImageCategorisations.strength.desc()).all()
        urls = [image.url for image in images]
        category_name = categories.subject_categories[category]
        return render_template('home.html', urls=urls, category_name=category_name, categories=categories.subject_categories)
    else:
        return redirect("/", code=302)
