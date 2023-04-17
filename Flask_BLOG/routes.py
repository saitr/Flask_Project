import os
from flask import Flask,render_template, url_for ,flash,redirect, request, abort

from Flask_BLOG.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm


from Flask_BLOG.models import User, Post

from Flask_BLOG import app,db, bcrypt
 
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from PIL import Image



@app.route('/')
@login_required
def hello():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    # return '<h1> Hey World!</h1>'
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='About')
    
@app.route('/register',methods=['GET','POST'])
def register():
    
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password  = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"You are now able to login go ahead! ",'success')

        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)


@app.route('/login', methods=['POST','GET'])
def login():
    
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember = form.rememberme.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("hello"))
        else:
            flash('Login Failed and Please Check Email and Password', 'danger')
    return render_template('login.html',title='Register',form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+ f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    
    form_picture.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file, form = form)





@app.route('/post/new',methods= ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content = form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(' Your post has been created successfully', 'success')
        return redirect(url_for('hello'))
    return render_template('create_post.html',title='New Post',form=form, legend='New Post')
 

@app.route("/post/<int:post_id>")
def post(post_id):
    # post = Post.query.get(post_id) # this just get the post
    post = Post.query.get_or_404(post_id)  # this gets the post if exitst otherwise gives 404 error
    return render_template('post.html',title= post.title, post=post, )




@app.route('/post_update/<int:post_id>',methods = ['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated successfully','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html',title= 'Update_Post',form = form,legend = 'Update Post')



@app.route('/post_delete/<int:post_id>/',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted','success')

    return redirect(url_for('hello'))



@app.route('/user/<string:username>')
@login_required
def user_posts(username): 
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username= username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=5)
    # return '<h1> Hey World!</h1>'
    return render_template('user_post.html',posts=posts,user=user)