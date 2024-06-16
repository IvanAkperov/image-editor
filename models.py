import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, LargeBinary, DateTime, func

db = SQLAlchemy()


class UserProfile(UserMixin, db.Model):
    """
    Model representing a user profile.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user, must be unique and not nullable.
        password (str): The password of the user, not nullable.
        email (str): The email of the user, must be unique and not nullable.
        photos (List[Photo]): A list of photos associated with the user.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    photos: Mapped[List['Photo']] = relationship('Photo', backref='user_profile', lazy=True)


class Photo(db.Model):
    """
    Model representing a photo.

    Attributes:
        id (int): The unique identifier for the photo.
        user_id (int): The identifier of the user who owns the photo.
        image_data (bytes): The binary data of the image, not nullable.
        created_at (datetime): The timestamp when the photo was created.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user_profile.id'), nullable=False)
    image_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.current_timestamp())