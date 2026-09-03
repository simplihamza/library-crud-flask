# Library Project

A small Flask web app for tracking books: view your library on the home page
and add new books through a form. Built while practicing Flask routing and
laying the groundwork for a real SQLite-backed persistence layer.

## Features

- View all books in the library on the home page (`/`), showing title,
  author, and rating out of 5.
- Friendly empty-state message ("Library is empty.") when no books have been
  added yet.
- Add a new book through a form (`/add`), submitting title, author, and
  rating, then redirecting back to the home page.

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

- **No persistence.** Books are stored in a plain Python list
  (`all_books = []`) in server memory. Restarting the Flask server wipes the
  entire library, there is no database wired up yet.
- **No edit or delete.** Once a book is added there is no way to change its
  rating or remove it from the UI.
- **No input validation.** The rating field is a plain text input; nothing
  stops a non-numeric or out-of-range value from being submitted.
- **No duplicate checking.** The same title can be added more than once.

## Planned / Next Steps

These are called out as TODOs directly in `main.py` and `playground.py` and
are not implemented yet:

- Replace the in-memory list with a real SQLAlchemy setup (`DeclarativeBase`,
  a `books.db` SQLite database, the Flask-SQLAlchemy extension).
- Define a `Book` model (id, title, author, rating) with proper constraints
  (unique title, not-null fields, correct types).
- Create the table schema on startup and update the `home` and `add` routes
  to read from and write to the database instead of the list.
- Add an `edit` route (GET/POST) to update a book's rating.
- Add a `delete` route to remove a book.
- Add "Edit Rating" and "Delete" links next to each book in `index.html`.
- Once implemented, explicitly verify persistence: add books, restart the
  server, confirm they're still there; cross-check `books.db` in DB Browser
  for SQLite after edits and deletes.

## What I Learned

- How to structure a basic Flask app: a `home` route that renders a template
  with data, and an `add` route that handles both displaying a form (GET)
  and processing its submission (POST) in the same view function, using
  `request.form` to read submitted fields and `redirect(url_for(...))` to
  send the user back to the home page afterward.
- Started comparing two ways of talking to a database in `playground.py`:
  raw `sqlite3` (connection, cursor, hand-written SQL strings) versus
  SQLAlchemy's Core layer (`engine`, `MetaData`, `Table`, `Column`) for
  defining and creating tables in code instead of raw SQL strings.
- Understood *why* the current library disappears on every restart: the
  book list lives only in a Python variable in server memory, not on disk.
  That's the concrete motivation for the SQLAlchemy/SQLite migration listed
  above.
