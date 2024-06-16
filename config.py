import os


class Config:
    """
    Configuration settings for the application.

    Attributes:
        ALLOWED_EXTENSIONS (set): A set of allowed file extensions for image uploads.
        SQLALCHEMY_DATABASE_URI (str): The URI for the SQLAlchemy database.
        SECRET_KEY (str): The secret key used for various security-related functions.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): A flag to disable SQLAlchemy track modifications.
    """
    ALLOWED_EXTENSIONS: set = {'png', 'jpg', 'jpeg'}
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postgres:excorpse@localhost/dbname'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'never-guess')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False