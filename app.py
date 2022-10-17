"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def user_redirect():
    """Redirect to users page"""
    
    return redirect('/users')

@app.route('/users')
def users_page():
    """List of users by name"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user_page():
    """Display form to add new user"""

    return render_template('new-user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Add new user to database and redirect back to users page"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show details about selected user"""

    user = User.query.get_or_404(user_id)

    return render_template("user-details.html",user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Show edit user form"""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html",user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Published edited user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user and redirect to users page"""

    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/post/<int:post_id>')
def post_details(user_id, post_id):
    """Show details about selected post"""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template("post-details.html",user=user, post=post)

@app.route('/users/<int:user_id>/new-post')
def add_post_page(user_id):
    """Display form to add new post"""

    user = User.query.get_or_404(user_id)

    return render_template('new-post.html', user=user)

@app.route('/users/<int:user_id>/new-post', methods=["POST"])
def publish_post_page(user_id):
    """Add new post to db, then redirect to user details page."""

    title = request.form["title"]
    content = request.form["content"]
    
    edited_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(edited_post)
    db.session.commit()

    user = User.query.get_or_404(user_id)

    return render_template("user-details.html",user=user)

@app.route('/users/<int:user_id>/post/<int:post_id>/edit')
def edit_post(user_id, post_id):
    """Form to edit selected post"""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template("edit-post.html",user=user, post=post)

@app.route('/users/<int:user_id>/post/<int:post_id>/edit', methods=["POST"])
def publish_edit(user_id, post_id):
    """Publish edited post to database and redirect back to users page"""

    Post.query.filter_by(id=post_id).delete()
    
    title = request.form["title"]
    content = request.form["content"]
    
    edited_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(edited_post)
    db.session.commit()

    user = User.query.get_or_404(user_id)

    return render_template("post-details.html", user=user, post=edited_post)

@app.route('/users/post/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post and redirect to users page"""

    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect('/users')

@app.route('/tags')
def list_tags():
    """List all tags."""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """Show details about selected tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag-details.html", tag=tag)

@app.route('/tags/new', methods=["POST"])
def publish_tag():
    """Navigate to create tag form"""

    name = request.form["name"]

    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/new')
def add_tag():
    """Navigate to create tag form"""

    return render_template("new-tag.html")

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Navigate to edit tag form"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit-tag.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def publish_edit_tag(tag_id):
    """Publish edited tag"""

    name = request.form["name"]

    edited_tag = Tag.query.filter_by(id=tag_id).first()

    edited_tag.name = name

    db.session.add(edited_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete tag and redirect to tags page"""

    Tag.query.filter_by(id=tag_id).delete()

    db.session.commit()

    return redirect('/tags')