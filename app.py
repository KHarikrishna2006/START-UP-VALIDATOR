from flask import Flask, render_template, request, redirect, url_for, session, g, flash
import sqlite3
from pathlib import Path
from validator import validate_idea

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "startup_validator.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idea_id INTEGER NOT NULL,
            market_score REAL NOT NULL,
            competition_score REAL NOT NULL,
            trend_score REAL NOT NULL,
            swot_strengths TEXT,
            swot_weaknesses TEXT,
            swot_opportunities TEXT,
            swot_threats TEXT,
            feasibility_score REAL NOT NULL,
            improvement_tips TEXT,
            FOREIGN KEY(idea_id) REFERENCES ideas(id)
        );
        """
    )
    db.commit()
    db.close()


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
        return
    db = get_db()
    g.user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    if g.user:
        db = get_db()
        history = db.execute(
            """
            SELECT ideas.id, ideas.title, ideas.created_at, predictions.feasibility_score
            FROM ideas
            LEFT JOIN predictions ON ideas.id = predictions.idea_id
            WHERE ideas.user_id = ?
            ORDER BY ideas.created_at DESC
            """,
            (g.user["id"],),
        ).fetchall()
    else:
        history = []
    return render_template("index.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
        ).fetchone()

        if user is None:
            db.execute(
                "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            db.commit()
            user = db.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password),
            ).fetchone()

        session["user_id"] = user["id"]
        flash("Logged in successfully.", "success")
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("index"))


@app.route("/submit_idea", methods=["GET", "POST"])
def submit_idea():
    if g.user is None:
        flash("Please log in to submit an idea.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if not title or not description:
            flash("Both title and description are required.", "danger")
            return render_template("submit_idea.html")

        db = get_db()
        cursor = db.execute(
            "INSERT INTO ideas (user_id, title, description) VALUES (?, ?, ?)",
            (g.user["id"], title, description),
        )
        idea_id = cursor.lastrowid

        result = validate_idea(title, description)
        db.execute(
            """
            INSERT INTO predictions (
                idea_id, market_score, competition_score, trend_score,
                swot_strengths, swot_weaknesses, swot_opportunities, swot_threats,
                feasibility_score, improvement_tips
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                idea_id,
                result["market_score"],
                result["competition_score"],
                result["trend_score"],
                "\n".join(result["swot"]["strengths"]),
                "\n".join(result["swot"]["weaknesses"]),
                "\n".join(result["swot"]["opportunities"]),
                "\n".join(result["swot"]["threats"]),
                result["feasibility_score"],
                "\n".join(result["improvement_tips"]),
            ),
        )
        db.commit()

        return redirect(url_for("result", idea_id=idea_id))

    return render_template("submit_idea.html")


@app.route("/result/<int:idea_id>")
def result(idea_id: int):
    if g.user is None:
        return redirect(url_for("login"))

    db = get_db()
    row = db.execute(
        """
        SELECT ideas.title, ideas.description, predictions.*
        FROM ideas
        JOIN predictions ON ideas.id = predictions.idea_id
        WHERE ideas.id = ? AND ideas.user_id = ?
        """,
        (idea_id, g.user["id"]),
    ).fetchone()

    if row is None:
        flash("Result not found.", "danger")
        return redirect(url_for("index"))

    data = dict(row)
    swot = {
        "strengths": data["swot_strengths"].split("\n") if data["swot_strengths"] else [],
        "weaknesses": data["swot_weaknesses"].split("\n") if data["swot_weaknesses"] else [],
        "opportunities": data["swot_opportunities"].split("\n") if data["swot_opportunities"] else [],
        "threats": data["swot_threats"].split("\n") if data["swot_threats"] else [],
    }
    tips = data["improvement_tips"].split("\n") if data["improvement_tips"] else []

    return render_template("result.html", data=data, swot=swot, tips=tips)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
