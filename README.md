# Library Project

A small Flask web app for tracking books: view your library on the home page,
add new books through a form, and edit or delete existing ones. Books are
stored in a SQLite database via SQLAlchemy, so they persist across server
restarts.

## Features

- View all books in the library on the home page (`/`), showing title,
  author, and rating out of 5.
- Friendly empty-state message ("Library is empty.") when no books have been
  added yet.
- Add a new book through a form (`/add`), submitting title, author, and
  rating, then redirecting back to the home page.
- Edit a book's rating via the "Edit Rating" link next to it (`/edit`),
  shows the book's current title and rating and updates just the rating on
  submit.
- Delete a book via the "Delete Book" link next to it (`/delete`), removes
  it from the database immediately.
- Books are stored in a real SQLite database (`books.db`) via a SQLAlchemy
  `Book` model, not an in-memory list, so they survive a server restart.
- Rating input is validated: submitting a non-numeric value or one outside
  0-5 re-shows the form with an error message instead of hitting the
  database.
- Submitting a duplicate book title shows a friendly error message instead
  of crashing, the database's unique constraint on `title` is caught and
  handled.
- Books on the home page are sorted alphabetically by title.

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

- **No delete confirmation.** The "Delete Book" link removes a book
  immediately with no confirmation step and no way to undo it.

## Planned / Next Steps

- Explicitly verify persistence: add a few books through the site, restart
  the server, and confirm they're still there.

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
- **Template filename mismatch.** `render_template("edit_rating.html", ...)`
  in the `edit` route raised `jinja2.exceptions.TemplateNotFound:
  edit_rating.html`, the actual template file was named `edit.html`. Fixed
  by matching the `render_template()` call to the real filename.
- **Calling `request.form` instead of indexing it.**
  `request.form("book_id")` raised `TypeError: 'ImmutableMultiDict' object
  is not callable`, `request.form` is a dict-like object, not a function.
  Fixed by switching to subscript access (`request.form["book_id"]`), the
  same syntax already used correctly in the `add` route.
- **Form field name mismatch.** After fixing that syntax, the same line
  still failed with `werkzeug.exceptions.BadRequestKeyError: 'book_id'`,
  because `edit.html`'s hidden input was named `id`, not `book_id`. Fixed
  by reading `request.form["id"]` to match the actual form field name.
