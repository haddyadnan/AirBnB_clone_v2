#!/usr/bin/python3
"""This module defines a class User"""
import os

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    __tablename__ = "users"

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        email = ""
        password = ""
        first_name = ""
        last_name = ""
    else:
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
