from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

#TABLE INFORMATION ARE PLACED HERE.
class Contact (Base):
	__tablename__ = 'contact'
	id = Column(Integer, primary_key=True)
	name = Column(String(60))
	email = Column(String(60))
	messege = Column(String(250))


class User (Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	first_name = Column(String(60))
	last_name = Column(String(60))
	username = Column(String(60), unique=True)
	password = Column(String(60))
	email = Column(String(140))

class Picture(Base):
	__tablename__='picture'
	id = Column(Integer, primary_key=True)
	pic1 = Column(String(150))
	pic2 = Column(String(150))
	pic3 = Column(String(150))
	pic4 = Column(String(150))