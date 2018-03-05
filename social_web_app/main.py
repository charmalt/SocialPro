# TODO: User Profile
# TODO: Posting Page
# TODO: Login Page
# TODO: Feed Page
# TODO: User view page (Admin)

# TDD Create Flask app with Hello World
# - Test check if hello world is returned
# - In the test,
#       run the app
#       call the /hello_world endpoint
#       assert the contents it returns has hello world
# Requests library - allows you to get content/ post things from endpoint

from flask import Flask, render_template, request, url_for, redirect
from flask_login import current_user
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_sqlalchemy import SQLAlchemy

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://social_pro:Blue24@localhost/social_pro'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database connection object
db = SQLAlchemy(app)


# Views
@app.route('/')
@login_required
def index():
    return 'Welcome to Social App. You are logged in.'


@app.route('/posting')
@login_required
def post():
    now_user = User.query.filter_by(email=current_user.email).first()
    return render_template('add_post.html', now_user=now_user)


@app.route('/user_list')
@login_required
def get_user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/add_post', methods=["POST"])
def add_post():
    post = Post(request.form['pcontent'], request.form['pemail'])
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/feed')
@login_required
def post_feed():
    singlePost = Post.query.all()
    return render_template('post_feed.html', singlePost=singlePost)


# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    post_content = db.Column(db.String(200))
    post_by = db.Column(db.String(50))

    def __init__(self, post_content, post_by):
        self.post_by = post_by
        self.post_content = post_content

    def __repr__(self):
        return '<Post %r>' % self.post_content


# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='test@xyz.com', password='test123')
    db.session.commit()


if __name__ == '__main__':
    app.run()
