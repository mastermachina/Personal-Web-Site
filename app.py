from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
# flask run
app = Flask(__name__)
#create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
# photo
picFolder = os.path.join('static', 'images') 
app.config['UPLOAD_FOLDER'] = picFolder


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return  'Blog post' + str(self.id)

@app.route('/')
def index(name = None):
    return render_template("index.html", name="Dogukan")

@app.route('/posts', methods = ['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content = post_content, author= 'Dogukan')
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template("posts.html", posts= all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post=BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        post=BlogPost.query.get_or_404(id)
        post.title = request.form['title']
        post.title = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html')

@app.route('/me', methods=['GET', 'POST'])
def about():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'me.jpg')
    return render_template('me.html', user_image= pic1)

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

if "__main__" == __name__:
    app.run(debug=True)