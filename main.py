from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from sqlalchemy.exc import IntegrityError

MIN_RATING = 0.0
MAX_RATING = 5.0

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


def parse_rating(raw_rating):
    """Return raw_rating as a float within [MIN_RATING, MAX_RATING], or None if invalid."""
    try:
        rating = float(raw_rating)
    except (TypeError, ValueError):
        return None
    if rating < MIN_RATING or rating > MAX_RATING:
        return None
    return rating


@app.route('/')
def home():
    return render_template('index.html', books=Book.query.order_by(Book.title).all())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        rating = parse_rating(request.form["rating"])
        if rating is None:
            return render_template(
                "add.html",
                error=f"Rating must be a number between {MIN_RATING} and {MAX_RATING}.",
            )

        with app.app_context():
            new_book = Book(title=request.form["title"], author=request.form["author"], rating=rating)
            db.session.add(new_book)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return render_template(
                    "add.html",
                    error=f"A book titled '{request.form['title']}' already exists.",
                )

        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)

        rating = parse_rating(request.form["rating"])
        if rating is None:
            return render_template(
                "edit.html",
                book=book_to_update,
                error=f"Rating must be a number between {MIN_RATING} and {MAX_RATING}.",
            )

        book_to_update.rating = rating
        db.session.commit()
        return redirect(url_for("home"))
    book_id = request.args.get("id")
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)

@app.route("/delete", methods=["GET"])
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)