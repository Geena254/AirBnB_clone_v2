#!/usr/bin/python3
"""Defines ``DBStorage`` class """

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """Class to manage storage of hbnb models in sql dbs """
    __engine = None
    __session = None

    def __init__(self):
        """starts the sql db storage"""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}:3306/{}'.format(user, passwd, host, database), pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns dict of the models stored in our db """

        class_dict = {}
        class_list = []
        if cls:
            class_list += [cls]
        else:
            class_list += [State, City, User, Place, Review, Amenity]
        for obj in class_list:
            for instance in self.__session.query(obj).all():
                key = instance.__class__.__name__ + "." + instance.id
                class_dict[key] = instance

        return class_dict

    def new(self, obj):
        """Adds a new object to our storage db """
        self.__session.add(obj)
        # self.save()

    def save(self):
        """commits the changes in the db """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object in the db sesssion """
        if obj:
            self.__session.delete(obj)
            # self.save()

    def reload(self):
        """reinitializes the storage db """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Closes the storage db"
        """
        self.__session.close()
