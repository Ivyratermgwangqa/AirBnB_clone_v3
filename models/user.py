#!/usr/bin/python3
""" holds class User"""
import hashlib
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models

class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)
        if kwargs.get('password'):
            self.password = self._hash_password(kwargs['password'])

    def _hash_password(self, password):
        """Hashes the password using MD5"""
        return hashlib.md5(password.encode()).hexdigest()

    def to_dict(self):
        """Returns a dictionary representation of the User instance"""
        user_dict = super().to_dict()
        user_dict.pop('password', None)  # Remove password from the dictionary
        return user_dict
