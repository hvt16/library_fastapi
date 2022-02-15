# Library Management
Backend implementaion for a small application of school library management system using FastAPI.


## Deployment

To start the server run :

```bash
  uvicorn main:app --reload
```



## Database Tables and Their Fields

#### Students
- student_id (int)
- name (string)
- email (string)
- password (string)
- issued_book (int): number of books issued.
- transaction (DB relationship)

#### Books
- book_id (int)
- title (string)
- description (string)
- transaction (DB relationship)

#### Inventory
- inv_id (int)
- book_id (int): Foreign Key for books.book_id
- availablity (bool)

#### Transaction
- transaction_id (int)
- tstudent (DB relationship): Mapping to the Students table.
- tstudent_id (int): Foreign Key for Students.student_id
- tbook (DB relationship): Mapping to the Books table.
- tbook_id (int): Foreign Key for Books.book_id


## Directory Structure
```bash
├── library
│   ├── __init__.py
│   ├── crud.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── main.py
