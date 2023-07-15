"""Blogly application."""
from flask import Flask, render_template, redirect, request # flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Post, PostTag, Tag, db, connect_db 

# Create a FLASK instance
app = Flask(__name__)
# Add a DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# SECRET KEY
app.config['SECRET_KEY'] = "hyptokrypo"
# DEBUG TOOLBAR
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# initializes the Flask Debug Toolbar
debug = DebugToolbarExtension(app)
# connect to DATABASE
connect_db(app)

#Create some users
first_name = ['fluffy', 'stevie', 'carole', 'sira', 'sally', 'bella', 'lucy']
last_name = ['hafer', 'wonder', 'baskin', 'baskin', 'struthers', 'ronder', 'ricardo']
users = [User(first_name=first, last_name=last) for first, last in zip(first_name, last_name)]

#Create some posts
post1 = Post(title='My first post', content='This is my first post', user_id=1)
post2 = Post(title='My second post', content='This is my second post', user_id=1)

#Create some tags
tag1 = Tag(name='funny')
tag2 = Tag(name='sad')
tag3 = Tag(name='happy')
tag4 = Tag(name='angry')

# Drop and recreate tables
with app.app_context():
	db.drop_all()
	db.create_all()
	for user in users:
		existing_user = User.query.filter_by(first_name=user.first_name).first() and User.query.filter_by(last_name=user.last_name).first()
		if not existing_user:
			db.session.add(user)
            
	db.session.commit()
	db.session.add_all([post1, post2, tag1, tag2, tag3, tag4])
	db.session.commit()

#----- ROUTES -----#
@app.route('/')
def home():
	'''home page'''
	users = User.query.all()
	posts = Post.query.all()
	tags = Tag.query.all()
	return render_template('home.html', users=users, posts=posts, tags=tags)


####################	USERS		####################
########################################################
@app.route('/users')
def list_users():
	'''List all users'''
	users = User.query.all()
	posts = Post.query.all()
	tags = Tag.query.all()
	return render_template('users.html', users=users, posts=posts, tags=tags)

@app.route('/users/new')
def show_user_form():
	'''Show add user form'''
	return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_user():
	'''Add a new User'''
	first_name = request.form['first_name'].lower()
	last_name = request.form['last_name'].lower()
	image_url = request.form['image_url'] or None
	new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
	db.session.add(new_user)
	db.session.commit()
	return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
	'''Show more details of a user'''
	user = User.query.get_or_404(user_id)
	posts = Post.query.all()
	tags = Tag.query.all()
	return render_template('user.html', user=user, posts=posts, tags=tags)

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
	'''Show edit user form'''
	user = User.query.get_or_404(user_id)
	return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_form(user_id):
	'''Edit user form'''
	user = User.query.get_or_404(user_id)
	user.first_name = request.form['first_name'].lower()
	user.last_name = request.form['last_name'].lower()
	user.image_url = request.form['image_url']

	db.session.commit()
	return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
	'''Delete a user'''
	user = User.query.get_or_404(user_id)
	db.session.delete(user)
	db.session.commit()
	return redirect('/users')




####################	POSTS		####################
########################################################
@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
	'''Show add post form'''
	user = User.query.get_or_404(user_id)
	tags = Tag.query.all()
	return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
	'''Add a new post'''
	user = User.query.get_or_404(user_id)
	title = request.form['title']
	content = request.form['content']

	tag_ids = [int(num) for num in request.form.getlist('tags') if num]
	tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

	new_post = Post(title=title, content=content, user_id=user.id, tags=tags)
	db.session.add(new_post)
	db.session.commit()

	# flash(f"Post '{new_post.title}' added.")

	return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
	'''Show a post'''
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
	'''Show edit post form'''
	post = Post.query.get_or_404(post_id)
	tags = Tag.query.all()
	return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
	'''Edit post'''
	post = Post.query.get_or_404(post_id)
	post.title = request.form['title']
	post.content = request.form['content']
	tag_ids = [int(num) for num in request.form.getlist('tags') if num]
	post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
	
	db.session.commit()
	return redirect(f"/users/{post.user_id}")  

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	'''Delete a post'''
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	return redirect(f"/users/{post.user_id}")



#################### TAGS ####################
###############################################
@app.route('/tags')
def all_tags():
	"""lists all tags"""
	tags = Tag.query.all()
	return render_template("all_tags.html", tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
	"""details of a tag and delete or edit tag"""
	tag = Tag.query.get_or_404(tag_id)
	return render_template("tag.html", tag=tag)

@app.route('/tags/new')
def show_new_tag_form():
	"""form for a new tag"""
	posts = Post.query.all()
	return render_template("new_tag.html", posts=posts)

@app.route('/tags/new', methods=['POST'])
def new_tag():
	"""form for a new tag"""

	post_ids = [int(num) for num in request.form.getlist('posts')]
	posts = Post.query.filter(Post.id.in_(post_ids)).all()
	name = request.form["name"]
	new_tag = Tag(name=name, posts=posts)
 
	db.session.add(new_tag)
	db.session.commit()
	return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
	"""form for a new tag"""
	tag = Tag.query.get_or_404(tag_id)
	posts = Post.query.all()
	return render_template("edit_tag.html", tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
	"""edit tag"""
	tag = Tag.query.get_or_404(tag_id)
	tag.name = request.form["name"]
	post_ids = [int(num) for num in request.form.getlist('posts')]
	tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

	db.session.commit()
	return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
	"""delete tag"""
	delete_tag = Tag.query.get_or_404(tag_id)
	db.session.delete(delete_tag)
	db.session.commit()
	return redirect('/tags')


##################################
##################################
##################################

@app.route('/phones')
def list_phones():
	"""List all phones"""
	emps = Employee.query.all()
	return render_template('phones.html')

@app.route('/snacks/new/', methods=["GET", "POST"])
def add_snack():
	form = AddSnackForm()
	if form.validate_on_submit():
		name = form.name.data
		price = form.price.data
		flash(f"Created new snack: {name} costs ${price}")
		return redirect('/phones')
	else:
		return render_template('add_snack_form.html', form=form)


# Run the app
if __name__ == '__main__':
	app.run()

