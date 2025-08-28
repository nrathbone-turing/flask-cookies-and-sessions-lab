#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize page_views if it's not set yet
    if 'page_views' not in session:
        session['page_views'] = 0

    # Increment for every request
    session['page_views'] += 1

    # Indicate if they've hit the limit
    if session['page_views'] > 3:
        return make_response(
            jsonify({'message': 'Maximum pageview limit reached'}), 401
        )

    # Otherwise, return the article
    article = Article.query.get(id)
    if article:
        return make_response(ArticleSchema().dump(article), 200)
    else:
        return make_response({'message': 'Article not found'}, 404)


if __name__ == '__main__':
    app.run(port=5555)
