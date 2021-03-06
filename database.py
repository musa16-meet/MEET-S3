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
	location = Column(String(60))
	picture = Column(String(150))
	question = Column(String(150))
	A1 = Column(String(100))
	A2 = Column(String(100))
	A3 = Column(String(100))

