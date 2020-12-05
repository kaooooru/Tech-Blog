from datetime import datetime

import requests
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://:vickyhhuang:@localhost:5432/techblog"
db = SQLAlchemy(app)

class BlogPost(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    content = db.Column(db.String)
    date_post = db.Column('timestamp', db.DateTime, default=datetime.now())

@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts = posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def add_post():
    title = request.form.get('title')
    author = request.form.get('author')
    content = request.form.get('content')

    post = BlogPost(title=title, author=author, content=content)
    db.session.add(post)
    db.session.commit()
    return redirect('/')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/news')
def news():
    url = ('http://newsapi.org/v2/top-headlines?country=us&apiKey=7f40cc2f9cad4c8dac50a30dc08bf958')
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    return render_template('news.html', articles=articles)