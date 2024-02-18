from sqlalchemy import create_engine, String, Integer, Column, ForeignKey
from sqlalchemy.orm import declarative_base


engine = create_engine('sqlite:///streaming.db')
Base = declarative_base()

class UserDb(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    plan = Column(String, nullable=False)


class Media(Base):

    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    plan = Column(String(50), nullable=False)
    category = Column(ForeignKey('category.name'))


class Category(Base):

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


Base.metadata.create_all(engine)