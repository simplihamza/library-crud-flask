# Library Project

A small Flask web app for tracking books: view your library on the home page
and add new books through a form. Books are stored in a SQLite database via
SQLAlchemy, so they persist across server restarts.

## Features

- View all books in the library on the home page (`/`), showing title,
  author, and rating out of 5.
- Friendly empty-state message ("Library is empty.") when no books have been
  added yet.
- Add a new book through a form (`/add`), submitting title, author, and
  rating, then redirecting back to the home page.
- Books are stored in a real SQLite database (`books.db`) via a SQLAlchemy
  `Book` model, not an in-memory list, so they survive a server restart.

## How to Run

1. Clone this repository and open a terminal in the project folder.
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   python main.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Known Issues / Limitations

- **No edit or delete.** Once a book is added there is no way to change its
  rating or remove it from the UI.
- **No input validation.** The rating field is a plain text input; nothing
  stops a non-numeric or out-of-range value from being submitted.
- **Duplicate titles crash instead of failing gracefully.** The `Book.title`
  column has a `unique=True` constraint, so submitting a title that already
  exists raises an unhandled `IntegrityError` (a server error page) instead
  of a friendly message.
- **Book list isn't ordered.** The home page renders `Book.query.all()` with
  no explicit ordering, so books show up in whatever order the database
  returns them, not alphabetically by title.

## Planned / Next Steps

These are called out as TODOs directly in `main.py` and are not implemented
yet:

- Add an `edit` route (GET/POST) to update a book's rating.
- Add a `delete` route to remove a book.
- Add "Edit Rating" and "Delete" links next to each book in `index.html`.
- Explicitly verify persistence: add a few books through the site, restart
  the server, and confirm they're still there.
- Once edit and delete exist, test them through the actual website UI and
  cross-check `books.db` in DB Browser for SQLite to confirm the underlying
  data actually changed.

## What I Learned

### Flask basics

- How to structure a basic Flask app: a `home` route that renders a template
  with data, and an `add` route that handles both displaying a form (GET)
  and processing its submission (POST) in the same view function, using
  `request.form` to read submitted fields and `redirect(url_for(...))` to
  send the user back to the home page afterward.
- Understood *why* the current library disappears on every restart: the
  book list lives only in a Python variable in server memory, not on disk.
  That's the concrete motivation for the SQLAlchemy/SQLite migration listed
  above.

### Database practice (`playground.py`)

- Compared two ways of talking to a database: raw `sqlite3` (connection,
  cursor, hand-written SQL strings) versus SQLAlchemy's Core layer
  (`engine`, `MetaData`, `Table`, `Column`) for defining and creating
  tables in code instead of raw SQL strings.
- Built a working Flask-SQLAlchemy ORM setup: a `DeclarativeBase` subclass,
  a `Book` model with typed columns (`Mapped[int]`, `Mapped[str]`,
  `Mapped[float]`) and real constraints (unique title, not-null fields),
  `db.create_all()` to build the schema, and a first `CREATE` (insert +
  commit) through the ORM.
- Learned that Flask-SQLAlchemy writes its SQLite file into an app-relative
  `instance/` folder by default (e.g. `instance/new-books-collection.db`),
  not the project root, useful to know when hunting for where the data
  actually landed.

### Errors hit and fixed

- **Python 3.14 vs. an outdated SQLAlchemy pin.** `SQLAlchemy==2.0.25`
  crashed on import under Python 3.14 with `AssertionError: ... directly
  inherits TypingOnly but has additional attributes`. Python 3.13+ added
  new automatic class attributes (`__firstlineno__`, `__static_attributes__`)
  that this older SQLAlchemy release's internal typing check didn't know how
  to ignore. Fixed by bumping `SQLAlchemy` to `2.0.52` (and `Flask` to
  `3.1.3` while at it) in `requirements.txt`, a dependency-version fix, no
  application code changed.
- **Column name mismatch.** The `Book` model defined a `review` column, but
  the code constructing a book passed `rating=...`. SQLAlchemy's generated
  `__init__` only accepts keyword arguments that match actual column names,
  so it raised `TypeError: 'rating' is an invalid keyword argument for
  Book`. Fixed by renaming the column to `rating` to match how it was
  being used.
- **Stale schema after the rename.** After fixing the column name,
  inserting a book still failed with `sqlite3.OperationalError: table book
  has no column named rating`. `db.create_all()` only creates tables that
  don't exist yet, it never alters an existing table's columns, and the
  old `instance/new-books-collection.db` from before the rename still had
  the table with the outdated `review` column. Fixed by deleting that
  stale `.db` file so `create_all()` rebuilt it fresh with the current
  schema.
