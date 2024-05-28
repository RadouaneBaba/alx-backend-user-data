#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """find a user by kwargs"""
        try:
            query = self._session.query(User).filter_by(**kwargs).one()
            return query
        except (InvalidRequestError, NoResultFound) as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user with user_id"""
        try:
            user = self.find_user_by(id=user_id)
            if not user:
                raise ValueError
            for key, value in kwargs.items():
                setattr(user, key, value)

            self._session.commit()
        except Exception:
            raise ValueError
