from pydantic import BaseModel
from typing import Optional, List

# different schema inheritence for data privacy

class BookBase(BaseModel):
	title : str 
	description : str 

# book schema for creation/addition of a new book
class BookCreate(BookBase):
	pass 

# book schema visible after post request
class Book(BookBase):
	book_id : int

	class Config:
		orm_mode = True

class StudentBase(BaseModel):
	name : str 
	email : str 

# schema for handling student registration 
class StudentCreate(StudentBase):
	password : str 

# this schema shows student details when neccessary
class Student(StudentBase):
	issued_books : int

	class Config:
		orm_mode = True

class Inventory(BaseModel):
	book_id = int 

	class Config:
		orm_mode = True 
