from dashboard.models.base import Base
from sqlalchemy import (
    Column,
    Integer,
    String)
from sqlalchemy.orm import synonym


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    pwd = Column(String(255), nullable=True)

    @property
    def password(self):
        return self.pwd

    @password.setter
    def password(self, value):
        from dashboard.security import pwd_context
        self.pwd = pwd_context.encrypt(value)

    password = synonym('pwd', descriptor=password)

    def check_password(self, password):
        from dashboard.security import pwd_context
        # always return false if password is greater than 255 to avoid
        # spoofing attacks
        if len(password) > 255:
            return False
        return pwd_context.verify(password, self.pwd)
