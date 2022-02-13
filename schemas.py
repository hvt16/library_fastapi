from pydantic import BaseModel
from typing import Optional, List

class Student(BaseModel):
	name : str 
	email : str 
	password : str

	class Config:
		orm_mode = True

class Book(BaseModel):
	title : str 
	description : str 

	class Config:
		orm_mode = True

class Inventory(BaseModel):
	book_id = int 

	class Config:
		orm_mode = True 