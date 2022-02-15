from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base 

# Student table
class Student(Base):
	__tablename__ = "students"
	student_id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	email = Column(String, unique=True, index=True)
	password = Column(String)
	issued_books = Column(Integer, default=0)
	# transaction relationship of issuing books
	transactions = relationship("Transaction", back_populates="tstudent")

# Books table
class Book(Base):
	__tablename__ = "books"
	book_id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String)
	# transaction relationship for issued books
	transactions = relationship("Transaction", back_populates="tbook")

# Inventory table
class Inventory(Base):
	__tablename__ = "inventory"	
	inv_id = Column(Integer, primary_key=True, index=True)
	book_id = Column(Integer, ForeignKey("books.book_id"), index=True)
	availablity = Column(Boolean, index=True, default=True)

# Transaction tables
class Transaction(Base):
	__tablename__ = "transaction"
	transaction_id = Column(Integer, primary_key=True, index=True)
	# student that holds the book
	tstudent = relationship("Student", back_populates="transactions")
	tstudent_id = Column(Integer, ForeignKey("students.student_id"), index=True)
	# issued book
	tbook = relationship("Book", back_populates="transactions")
	tbook_id = Column(Integer, ForeignKey("books.book_id"), index=True)
