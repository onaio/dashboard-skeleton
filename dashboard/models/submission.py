from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from dashboard.models.base import Base, BaseModelFactory


class SubmissionFactory(BaseModelFactory):
    pass


class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value