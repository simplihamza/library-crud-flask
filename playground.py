from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session

# ==================== sqlite3 practice ====================

# TODO-1: In a throwaway script (or reuse a section of playground.py),
#  import the built-in sqlite3 module and create a connection to a new
#  database file, this alone will create the .db file on disk when run.

# TODO-2: Create a cursor from that connection, this is what actually
#  executes commands against the database.

# TODO-3: Use the cursor to execute a raw SQL CREATE TABLE command,
#  defining a books table with four fields: id (integer primary key),
#  title (a string with a max length, required, unique), author (a
#  string with a max length, required), and rating (a float, required).

# TODO-4: Download DB Browser for SQLite, and open your new .db file with
#  it, so you can visually confirm the table was created correctly.

# TODO-5: Use the cursor to execute a raw SQL INSERT command adding one
#  book (e.g. Harry Potter) into the table, then commit the change so
#  it's actually saved to disk. Comment out or remove the CREATE TABLE
#  line before rerunning, otherwise you'll get an error since the table
#  already exists.

# TODO-6: Reopen the database in DB Browser (close it first if it was
#  already open, or you'll get a "database locked" warning) and confirm
#  your new row appears.

# TODO-7: Reflect on why this raw SQL approach is fragile, notice how
#  easy it would be to make an invisible typo (e.g. VALUE instead of
#  VALUES) that silently breaks things. This motivates the next section.

# ==================== SQLAlchemy (raw Table/Column) practice ====================

engine = create_engine('sqlite:///testdatabase.db', echo=True)

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

meta = MetaData()
users = Table('users', meta, Column('id', Integer, primary_key=True),
              Column('name', String, nullable=False)
              , Column('age', Integer))

meta.create_all(engine)

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