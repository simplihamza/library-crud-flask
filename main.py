from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html', books=Book.query.all())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
            db.session.add(new_book)
            db.session.commit()

        return redirect(url_for("home"))
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)

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