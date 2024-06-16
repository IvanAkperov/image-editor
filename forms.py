from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(FlaskForm):
    """
    A form for user registration.

    Attributes:
        name (StringField): A field for the user's name.
            - Validators: Length between 4 and 30 characters, DataRequired.
            - Placeholder: 'name'.
            - Style: Border with 1px solid.
        email (EmailField): A field for the user's email.
            - Validators: DataRequired, Email.
            - Placeholder: 'email'.
            - Style: Border with 1px solid.
        password (PasswordField): A field for the user's password.
            - Validators: DataRequired, Length between 8 and 24 characters.
            - Placeholder: 'password'.
            - Style: Border with 1px solid.
        password_repeat (PasswordField): A field for confirming the user's password.
            - Validators: DataRequired, Must match the 'password' field.
            - Placeholder: 'confirm password'.
            - Style: Border with 1px solid.
    """
    name: StringField = StringField("name", render_kw={'placeholder': 'name', 'style': 'border: 1px solid'},
                                    validators=[Length(min=4, max=30), DataRequired()])
    email: EmailField = EmailField("email", render_kw={'placeholder': 'email', 'style': 'border: 1px solid'},
                                   validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField("password", render_kw={'placeholder': "password", 'style': 'border: 1px solid'},
                                            validators=[DataRequired(), Length(min=8, max=24)])
    password_repeat: PasswordField = PasswordField("password_repeat",
                                                   render_kw={'placeholder': 'confirm password', 'style': 'border: 1px solid'},
                                                   validators=[DataRequired(), EqualTo('password')])


class LoginForm(FlaskForm):
    """
    A form for user login.

    Attributes:
        name (StringField): A field for the user's name.
            - Validators: Length between 4 and 30 characters, DataRequired.
            - Placeholder: 'name'.
            - Title: 'Enter your name'.
            - Autofocus: True.
            - Style: Border with 1px solid.
        password (PasswordField): A field for the user's password.
            - Validators: DataRequired, Length between 8 and 24 characters.
            - Placeholder: 'password'.
            - Title: 'Enter your password'.
            - Style: Border with 1px solid.
            - ID: 'password'.
            - Oninput: 'checkPasswordLength()'.
    """
    name: StringField = StringField("name", render_kw={'placeholder': 'name', 'title': 'Enter your name', 'autofocus': True,
                                                       'style': 'border: 1px solid'},
                                    validators=[Length(min=4, max=30), DataRequired()])
    password: PasswordField = PasswordField("password", render_kw={'placeholder': 'password', 'title': 'Enter your password',
                                                                   'style': 'border: 1px solid', 'id': 'password',
                                                                   'oninput': 'checkPasswordLength()'},
                                            validators=[DataRequired(), Length(min=8, max=24)])