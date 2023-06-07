# posts routes
from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Post
from tseg.posts.forms import PostForm
from tseg.users.forms import SearchForm

posts = Blueprint('posts', __name__)

@posts.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@posts.route("/post-new-<string:parent_name>-<string:parent_id>", methods=['GET', 'POST'])
@login_required # impide el acceso sin login
def new_post(parent_name, parent_id):
	form = PostForm()
	if form.validate_on_submit():
		post = Post(content=form.content.data, 
					author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Su mensaje se ha creado!', 'success')
		return redirect(url_for('posts.all_posts'))
	return render_template('create_post.html', title='Nuevo mensaje', 
												form=form,
												parent_name=parent_name,
												parent_id=parent_id,
												legend="Crear mensaje")


# ruteo de variables "post_id"
@posts.route("/post-<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template("post.html", post=post)


@posts.route("/post-<int:post_id>-update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403) #http forbidden
	form = PostForm()
	if form.validate_on_submit():
		post.content = form.content.data
		db.session.commit()
		flash("Su mensaje ha sido editado con éxito", 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.content.data = post.content
	return render_template('create_post.html', 	title='Editar mensaje', 
												form=form,
												legend="Editar mensaje")

@posts.route("/post-<int:post_id>-delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash("Su mensaje ha sido eliminado!", 'success')
	return redirect(url_for('posts.all_posts'))