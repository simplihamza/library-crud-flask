from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []

@app.route('/')
def home():
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = {
            "title": request.form["title"],
            "author": request.form["author"],
            "rating": request.form["rating"]
        }
        all_books.append(new_book)
        return redirect(url_for("home"))
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)


# TODO-13: Replace the in-memory 'all_books = []' list entirely with a
#  real SQLAlchemy setup: DeclarativeBase subclass, database URI pointing
#  to books.db, SQLAlchemy extension created and initialized with your
#  app, following the exact same pattern you just practiced.

# TODO-14: Define your Book model with the four fields (id, title,
#  author, rating), matching the constraints from your sqlite3/SQLAlchemy
#  practice (unique title, not-null fields, correct types).

# TODO-15: Create the table schema on startup, inside an app context.

# TODO-16: Update the 'home' route to query all books from the database
#  (ordered by title) instead of reading from the old list, and pass the
#  results into the template exactly as before.

# TODO-17: Update the 'add' route so that submitting the form creates a
#  new Book database record (instead of appending to a list), commits
#  it, and redirects to home on success, same behavior as before, just
#  backed by real persistence now.

# TODO-18: Create a new 'edit' route (GET and POST) that fetches a
#  specific book by ID, shows its current title/rating on GET, and
#  updates just its rating on POST, committing the change.

# TODO-19: Create a new 'delete' route that fetches a specific book by
#  ID and deletes it, committing the change, then redirects home.

# TODO-22: Add a few books through the website, confirm they appear.
#  Stop the Flask server completely, then restart it. Reload the home
#  page, if your books are now backed by a real database instead of the
#  old in-memory list, they should still be there, this is the entire
#  point of this project, confirm it explicitly rather than assuming it
#  works.

# TODO-23: Test edit and delete through the actual website UI, and
#  cross-check the books.db file directly in DB Browser to confirm the
#  underlying data actually changed.