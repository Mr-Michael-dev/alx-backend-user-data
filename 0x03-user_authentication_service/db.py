#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from typing import Dict

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict) -> User:
        """Find a user by email or hashed_password
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound as e:
            # Handle the NoResultFound exception
            raise e
        except InvalidRequestError as e:
            # Handle the InvalidRequestError exception
            raise e

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """
        Updates a user’s attributes and then commit changes to the database.

        Arguments:
        user_id - id of user to update
        **kwargs - key:value pairs of attributes to update

        Raises:
        ValueError if an invalid attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"User with id {user_id} not found")

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        try:
            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e
