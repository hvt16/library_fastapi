from sqlalchemy.orm import Session 
import models, schemas 

# get student from student_id
def get_student(db:Session, student_id:int):
	return db.query(models.Student).filter(models.Student.student_id == student_id).first()

#  get student from email
# while checking for an already registered student
def get_student_by_email(db : Session, email : str):
	return db.query(models.Student).filter(models.Student.email == email).first()

# student registration
def add_student(db : Session, student : schemas.StudentCreate):
	db_student = models.Student(name = student.name, 
		email = student.email, 
		password=student.password)
	db.add(db_student)
	db.commit()
	db.refresh(db_student)
	return db_student

# add new book to the library
def add_book(db: Session, book:schemas.BookCreate):
	db_book = models.Book(title=book.title, description=book.description)
	db.add(db_book)
	db.commit()
	db.refresh(db_book)

	# update inventory with new book's details
	add_book_inventory(db, db_book.book_id)
	return db_book

# return all registered books
def get_books(db: Session, limit : int = 100):
	return db.query(models.Book).limit(limit).all()

# return inventory's current status and availablity of books
def get_inventory(db: Session, limit : int = 100):
	return db.query(models.Inventory).limit(limit).all()

# inventory update
def add_book_inventory(db: Session, book_id: int):
	db_inv = models.Inventory(book_id = book_id)
	db.add(db_inv)
	db.commit()
	db.refresh(db_inv)
	return db_inv 

# function returns number of books that a student currently have
def issued_books_by_student(db: Session, student_id: int):
	student_db = db.query(models.Student).filter(models.Student.student_id == student_id).first()
	return student_db.issued_books

# book issue
def issue_book(db: Session, book_id: int, student_id: int):
	
	# transaction represents the data of book issue
	new_transaction = models.Transaction(tstudent_id = student_id, 
			tbook_id = book_id)
	db.add(new_transaction)
	db.commit()
	
	# update inventory with book availablity status
	inv_db = db.query(models.Inventory).filter(models.Inventory.book_id == book_id).first()
	inv_db.availablity = False
	db.commit()

	# update the number of books a student is holding right now
	student_db = db.query(models.Student).filter(models.Student.student_id == student_id).first()
	student_db.issued_books += 1
	db.commit()
	db.refresh(student_db)
	return student_db

# return book
def return_book(db: Session, book_id: int, student_id: int):

	# remove the issued book and its transaction data
	transaction_db = db.query(models.Transaction).filter(models.Student.student_id == student_id).first()
	db.delete(transaction_db)
	db.commit()

	# update the availablity of books in the inventory
	inv_db = db.query(models.Inventory).filter(models.Inventory.book_id == book_id).first()
	inv_db.availablity = True
	db.commit()

	# update the number of books a student is currently holding
	student_db = db.query(models.Student).filter(models.Student.student_id == student_id).first()
	student_db.issued_books -= 1
	db.commit()
	db.refresh(student_db)
	return student_db