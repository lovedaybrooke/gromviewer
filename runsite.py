from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

import categories

app = Flask(__name__)
heroku = Heroku(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def legit_category(url_slug):
    if url_slug in categories.ingredient_categories.keys():
        return url_slug, categories.ingredient_categories[url_slug]
    elif url_slug in categories.food_categories.keys():
        return url_slug, categories.food_categories[url_slug]
    elif url_slug in categories.people_categories.keys(): 
        return url_slug, categories.people_categories[url_slug]
    elif url_slug in categories.architecture_categories.keys(): 
        return url_slug, categories.architecture_categories[url_slug]
    elif url_slug in categories.style_categories.keys(): 
        return url_slug, categories.style_categories[url_slug]
    else:
        return False, False


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
    return render_template('home.html',
            ingredient_categories=categories.ingredient_categories,
            food_categories=categories.food_categories,
            people_categories=categories.people_categories,
            architecture_categories=categories.architecture_categories,
            style_categories=categories.style_categories
            )

@app.route('/test')
def test():
    return render_template('test.html',
            ingredient_categories=categories.ingredient_categories,
            food_categories=categories.food_categories,
            people_categories=categories.people_categories,
            architecture_categories=categories.architecture_categories,
            style_categories=categories.style_categories)

@app.route('/<category>', methods=['GET', 'POST'])
def category(category):
    category_slug, category_name = legit_category(category)
    if category_slug:
        confidence = request.args.get('confidence', default=50)
        images = ImageCategorisations.query.filter(
            ImageCategorisations.tag == category_slug).filter(
            ImageCategorisations.strength > float(confidence)/100).order_by(
            ImageCategorisations.strength.desc()).all()
        urls = [image.url for image in images]

        return render_template('category.html',
            urls=urls,
            confidence=confidence,
            count=len(urls),
            category_name=category_name,
            category_slug=category_slug,
            ingredient_categories=categories.ingredient_categories,
            food_categories=categories.food_categories,
            people_categories=categories.people_categories,
            architecture_categories=categories.architecture_categories,
            style_categories=categories.style_categories
            )
    else:
        return redirect("/", code=302)
