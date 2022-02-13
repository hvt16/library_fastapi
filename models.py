from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base 

class Student(Base):
	__tablename__ = "students"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	email = Column(String, unique=True, index=True)
	password = Column(String)

	# books will be added...

class Book(Base):
	__tablename__ = "books"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String)
	student_id = Column(Integer, ForeignKey("students.id"))

class Inventory(Base):
	__tablename__ = "inventory"
	
	id = Column(Integer, primary_key=True, index=True)
	book_id = Column(Integer, ForeignKey("books.id"))
	availablity = Column(Boolean, index=True, default=True)

