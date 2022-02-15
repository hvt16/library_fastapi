from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas 
from database import SessionLocal, engine

# create all database tables if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# database dependancy
def get_db():
	db = SessionLocal()
	try:
		yield db 
	finally:db.close()

# student registration
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session=Depends(get_db)):
	db_student = crud.get_student_by_email(db, email=student.email)
	# already registered email
	if db_student:
		raise HTTPException(status_code=400, detail="This email is alreadly registered")
	return crud.add_student(db=db, student=student)

# add new book 
@app.post("/books/", response_model=schemas.Book)
def add_book(book: schemas.BookCreate, db:Session=Depends(get_db)):
	return crud.add_book(db=db, book=book)

# find all registered books
@app.get("/books/")
def get_books(limit: int = 100, db: Session = Depends(get_db)):
	return crud.get_books(db=db, limit=limit)

# return all books registered in the library with their availablity
@app.get("/inventory/")
def get_inventory(limit: int = 100, db: Session = Depends(get_db)):
	books = crud.get_inventory(db, limit=limit)
	return books 

# a student (student_id) issues book (book_id)
@app.post("/issue_book/", response_model=schemas.Student)
def issue_book(student_id: int, book_id: int, db:Session=Depends(get_db)):
	total_issued = crud.issued_books_by_student(db=db, student_id=student_id)
	# can't issure more than 3 books
	if total_issued<3:
		return crud.issue_book(db=db, book_id=book_id, student_id=student_id)
	else:
		raise HTTPException(status_code=404, detail="A student can hold atmost 3 books at a time")

# a student returns book
@app.post("/return_book/", response_model=schemas.Student)
def return_book(student_id: int, book_id: int, db:Session = Depends(get_db)):
	total_issued = crud.issued_books_by_student(db=db, student_id=student_id)
	# can't return a book if there isn't any issued book
	if total_issued>0:
		return crud.return_book(db=db, book_id=book_id, student_id=student_id)
	else:
		raise HTTPException(status_code=404, detail="This student doesn't have any book")