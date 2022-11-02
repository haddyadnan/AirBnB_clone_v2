#!/usr/bin/python3

"""
Script for DBStorage integration
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm import sessionmaker
from models.base_model import Base


class DBStorage:
    """
    DBStorage class
    """

    __engine = None
    __session = None

    def __init__(self) -> None:

        HBNB_MYSQL_USER = os.getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = os.getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = os.getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = os.getenv("HBNB_MYSQL_DB")
        HBNB_ENV = os.getenv("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB
            ),
            pool_pre_ping=True,
        )

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session (self.__session) all objects
        depending of the class name (argument cls
        """
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User
        from models.amenity import Amenity

        classes = {
            "Amenity": Amenity,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User,
        }

        cls_name = ["User", "State", "City", "Amenity", "Place", "Review"]
        new_objects = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                try:
                    del obj._sa_instance_state
                except KeyError:
                    pass
                new_objects[key] = obj.__dict__
        else:
            for cls in cls_name:
                for obj in self.__session.query(classes[cls]).all():
                    key = obj.__class__.__name__ + "." + obj.id
                new_objects[key] = obj.__dict__
        return new_objects
        # new_dict = {}
        # for clss in classes:
        #     if cls is None or cls is classes[clss] or cls is clss:
        #         objs = self.__session.query(classes[clss]).all()
        #         for obj in objs:
        #             # key = obj.__class__.__name__ + "." + obj.id
        #             # new_dict[key] = obj
        #             priobj
        # return obj.__dict__

    def new(self, obj):
        """a
        dd the object to the current database session
        """

        self.__session.add(obj)

    def save(self):
        """
        commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
