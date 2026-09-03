from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session
import sqlite3

# ==================== sqlite3 practice ====================

db = sqlite3.connect("books-collection.db")
cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
db.commit()

# ==================== SQLAlchemy (raw Table/Column) practice ====================

# engine = create_engine('sqlite:///testdatabase.db', echo=True)

# connection = engine.connect()
# connection.execute(text("CREATE TABLE IF NOT EXISTS users(name TEXT, age INTEGER)"))
#
# connection.execute(text("INSERT INTO users (name, age) VALUES (:name, :age)"),
#                     {"name": "Hamza", "age": 25})
# connection.commit()
#
# result = connection.execute(text("SELECT * FROM users"))
# for row in result:
#     print(row)
#
# session = Session(engine)
# session.execute(text('INSERT INTO users(name, age) VALUES ("Sultan", 21);'))
#
# session.commit()

# meta = MetaData()
# users = Table('users', meta, Column('id', Integer, primary_key=True),
#               Column('name', String, nullable=False)
#               , Column('age', Integer))
#
# meta.create_all(engine)

# ==================== SQLAlchemy (Flask-SQLAlchemy ORM) practice ====================

# TODO-8: Set up requirements.txt with flask, SQLAlchemy, and
#  flask_sqlalchemy at the specified versions, and install them.

# TODO-9: In a fresh script, import Flask, SQLAlchemy, DeclarativeBase,
#  Mapped, mapped_column, and the column type classes you'll need
#  (Integer, String, Float).

# TODO-10: CHALLENGE (work through this yourself before checking the
#  reference pattern): using the Flask-SQLAlchemy documentation, figure
#  out how to initialize a db object, define a Book model with the same
#  four fields as before, and create the schema. Try this without
#  looking at a solution first, the goal is to practice reading official
#  docs and mapping them to what you already did manually with sqlite3.

# TODO-11: Once your table exists, practice each CRUD operation
#  separately, inside an app context each time:
#  - CREATE: instantiate a new Book object and add/commit it.
#  - READ ALL: build a select query ordered by title, execute it, and
#    extract the actual objects (not raw rows) from the result.
#  - READ ONE: build a select query filtered by a specific field (e.g.
#    title equals a specific value), and extract a single result rather
#    than a list of results.
#  - UPDATE: fetch a specific record (try both by matching a field value,
#    and separately by primary key), change one of its attributes, and
#    commit.
#  - DELETE: fetch a specific record by primary key and delete it,
#    committing afterward.

# TODO-12: Look specifically at the shortcut method Flask-SQLAlchemy
#  provides for fetching-by-primary-key-or-returning-a-404-automatically,
#  compare it to the manual "select where id equals" approach, and note
#  when you'd prefer one over the other.