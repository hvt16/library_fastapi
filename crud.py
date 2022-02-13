from sqlalchemy.orm import Session 
import models, schemas 

def get_student(db:Session, student_id:int):
	return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_email(db : Session, email : str):
	return db.query(models.Student).filter(models.Student.email == email).first()

def add_student(db : Session, student : schemas.Student):
	db_student = models.Student(name = student.name, 
		email = student.email, 
		password=student.password)
	db.add(db_student)
	db.commit()
	db.refresh(db_student)
	return db_student

def add_book(db: Session, book:schemas.Book):
	db_book = models.Book(title=book.title, description=book.description)
	db.add(db_book)
	db.commit()
	db.refresh(db_book)
	# // add this book to the inventory
	add_book_inventory(db, db_book.id)
	return db_book

def get_inventory(db: Session, limit : int = 100):
	return db.query(models.Inventory).limit(limit).all()


def add_book_inventory(db: Session, book_id: int):
	db_inv = models.Inventory(book_id = book_id)
	db.add(db_inv)
	db.commit()
	db.refresh(db_inv)
	return db_inv 