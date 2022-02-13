from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas 
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# dependancy
def get_db():
	db = SessionLocal()
	try:
		yield db 
	finally:db.close()

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.Student, db: Session=Depends(get_db)):
	db_student = crud.get_student_by_email(db, email=student.email)
	if db_student:
		raise HTTPException(status_code=400, detail="This email is alreadly registered")
	return crud.add_student(db=db, student=student)

@app.post("/books/", response_model=schemas.Book)
def add_book(book: schemas.Book, db:Session=Depends(get_db)):
	return crud.add_book(db=db, book=book)

@app.get("/inventory/", response_model=List[schemas.Inventory])
def get_inventory(limit: int = 100, db: Session = Depends(get_db)):
	books = crud.get_inventory(db, limit=limit)
	return books 