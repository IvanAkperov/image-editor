import io
import base64
from PIL import ImageFilter, Image
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from loguru import logger
from forms import RegisterForm, LoginForm
from models import db, UserProfile, Photo
from config import Config
from typing import Optional

app = Flask(__name__)
app.config.from_object(Config)
bcrypt = Bcrypt(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'you need to log in first'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id: str) -> Optional['UserProfile']:
    """
    Load a user from the database based on the user ID.

    Args:
        user_id (str): The ID of the user to load.

    Returns:
        Optional[UserProfile]: The user profile if found, otherwise None.
    """
    return UserProfile.query.get(int(user_id))


def allowed_file(filename: str) -> bool:
    """
    Check if the file extension is allowed.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file extension is allowed, otherwise False.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/")
def home() -> str:
    """
    Render the home page.

    Returns:
        str: The rendered HTML for the home page.
    """
    return render_template('base.html', title='Home')


@app.template_filter('b64encode')
def base64_encode(data: bytes) -> str:
    """
    Encode binary data to a base64 string.

    Args:
        data (bytes): The binary data to encode.

    Returns:
        str: The base64 encoded string.
    """
    return base64.b64encode(data).decode('utf-8')


@app.route("/create")
@login_required
def create() -> str:
    """
    Render the create page.

    Returns:
        str: The rendered HTML for the create page.
    """
    return render_template("create.html")


@app.route("/results/<int:photo_id>/")
@login_required
def results(photo_id: int) -> str:
    """
    Render the results page for a specific photo.

    Args:
        photo_id (int): The ID of the photo to display.

    Returns:
        str: The rendered HTML for the results page.
    """
    photo = Photo.query.get_or_404(photo_id)
    return render_template("results.html", photo=photo)


@app.route("/my_works")
@login_required
def my_works() -> str:
    """
    Render the page displaying all photos created by the current user.

    Returns:
        str: The rendered HTML for the my_works page.
    """
    page = request.args.get('page', 1, type=int)
    photos = Photo.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=5)
    return render_template("my_works.html", photos=photos)


@app.route("/delete/<int:photo_id>/", methods=['GET', 'POST'])
@login_required
def delete_photo(photo_id: int) -> 'Response':
    """
    Delete a specific photo and redirect to the my_works page.

    Args:
        photo_id (int): The ID of the photo to delete.

    Returns:
        Response: A redirect response to the my_works page.
    """
    photo = Photo.query.get_or_404(photo_id)
    db.session.delete(photo)
    db.session.commit()
    return redirect(url_for('my_works'))


@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload() -> 'Response':
    """
    Handle the upload of a photo and apply transformations based on user input.

    Returns:
        Response: A redirect response to the appropriate page.
    """
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part', 'info')
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '' or not allowed_file(file.filename):
            flash('Invalid file type', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            photo = Image.open(file.stream)
            value = request.form.get('value')
            if value == 'black-white':
                photo = photo.convert("L")
            elif value == 'blur':
                photo = photo.filter(ImageFilter.GaussianBlur(radius=2))
            elif value == 'left':
                photo = photo.rotate(90)
            elif value == 'right':
                photo = photo.rotate(270)
            elif value == 'sketch':
                photo = photo.convert("L").point(lambda p: 255 if p > 90 else p // 2)
            elif value == 'rotate':
                photo = photo.rotate(180)
            img_io = io.BytesIO()
            photo.save(img_io, 'JPEG' if file.filename.lower().endswith('.jpg') else 'PNG', quality=70)
            img_io.seek(0)
            new_photo = Photo(user_id=current_user.id, image_data=img_io.getvalue())
            db.session.add(new_photo)
            db.session.commit()
            flash('File successfully uploaded', 'success')
            return redirect(url_for("results", photo_id=new_photo.id))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    Returns:
        Response: A redirect response to the appropriate page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = UserProfile.query.filter_by(username=form.name.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Successfully logged in!", 'success')
            return redirect(url_for("create"))
        else:
            flash('Invalid username or password', 'danger')
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Handle user registration.

    Returns:
        Response: A redirect response to the appropriate page.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = UserProfile(username=form.name.data, password=hashed_pwd, email=form.email.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash("Successfully registered!", 'success')
            return redirect(url_for("create"))
        except Exception as e:
            db.session.rollback()
            logger.error(e)
            return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout() -> 'Response':
    """
    Handle user logout.

    Returns:
        Response: A redirect response to the login page.
    """
    logout_user()
    flash("Successfully logged out", 'success')
    return redirect(url_for("login"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
