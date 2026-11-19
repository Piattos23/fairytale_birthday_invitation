"""
Fairytale Birthday Invitation - Flask app

Run locally:
    pip install -r requirements.txt
    python app.py
Open:
    http://127.0.0.1:5000
Admin:
    http://127.0.0.1:5000/admin

For deployment, configure SECRET_KEY and ADMIN_PASSWORD.
For PostgreSQL, configure DATABASE_URL. Without it, SQLite is used.
"""

import os
import sqlite3
from functools import wraps

from flask import (
    Flask, flash, g, redirect, render_template, request,
    session, url_for
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-secret-key")

# ---------- EDIT THESE ----------
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

PARTY = {
    "host": "Cade G. Solo",
    "age": 25,
    "date": "Saturday, December 20, 2026",
    "time": "5:00 PM",
    "place": "Garden Pavilion, Bacolod City",
    "dress_code": "Pastel colors, florals & a little sparkle",
    "message": "Come hungry, bring your loudest laugh, and help me "
               "make this a night to remember.",
    "rsvp_by": "December 10",
}
# --------------------------------

DB_PATH = os.environ.get(
    "DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "rsvp.db"),
)
DATABASE_URL = os.environ.get("DATABASE_URL")
USE_PG = bool(DATABASE_URL)
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Manila")


def get_db():
    if "db" not in g:
        if USE_PG:
            import psycopg
            from psycopg.rows import dict_row
            g.db = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        else:
            g.db = sqlite3.connect(DB_PATH)
            g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    if USE_PG:
        import psycopg
        with psycopg.connect(DATABASE_URL, autocommit=True) as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS responses (
                       id SERIAL PRIMARY KEY,
                       name TEXT NOT NULL,
                       answer TEXT NOT NULL CHECK (answer IN ('Yes', 'No')),
                       answered_at TIMESTAMPTZ NOT NULL DEFAULT now()
                   )"""
            )
            db.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS responses_name_ci "
                "ON responses (LOWER(name))"
            )
    else:
        with sqlite3.connect(DB_PATH) as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS responses (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                       answer TEXT NOT NULL CHECK (answer IN ('Yes', 'No')),
                       answered_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
                   )"""
            )


def save_response(name, answer):
    db = get_db()
    if USE_PG:
        db.execute(
            """INSERT INTO responses (name, answer) VALUES (%s, %s)
               ON CONFLICT ((LOWER(name))) DO UPDATE SET
                   answer = EXCLUDED.answer, answered_at = now()""",
            (name, answer),
        )
    else:
        db.execute(
            """INSERT INTO responses (name, answer) VALUES (?, ?)
               ON CONFLICT(name) DO UPDATE SET
                   answer = excluded.answer,
                   answered_at = datetime('now', 'localtime')""",
            (name, answer),
        )
    db.commit()


def list_responses():
    db = get_db()
    if USE_PG:
        cur = db.execute(
            """SELECT id, name, answer,
                      to_char(answered_at AT TIME ZONE %s,
                              'YYYY-MM-DD HH12:MI AM') AS answered_at
               FROM responses ORDER BY id DESC""",
            (TIMEZONE,),
        )
    else:
        cur = db.execute(
            "SELECT id, name, answer, answered_at FROM responses ORDER BY id DESC"
        )
    return cur.fetchall()


def remove_response(response_id):
    db = get_db()
    db.execute(
        "DELETE FROM responses WHERE id = %s" if USE_PG
        else "DELETE FROM responses WHERE id = ?",
        (response_id,),
    )
    db.commit()


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    if request.args.get("change"):
        session.pop("guest", None)
        return redirect(url_for("index"))
    return render_template("index.html", party=PARTY, guest=session.get("guest"))


@app.route("/rsvp", methods=["POST"])
def rsvp():
    name = " ".join(request.form.get("name", "").split())[:60]
    answer = request.form.get("answer", "")

    if not name or answer not in ("Yes", "No"):
        flash("Please type your name before choosing Yes or No.", "error")
        return redirect(url_for("index"))

    save_response(name, answer)
    session["guest"] = {"name": name, "answer": answer}
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin"))
        flash("That password wasn't quite right. Please try again.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin():
    show = request.args.get("show", "all")
    rows = list_responses()

    yes = [r for r in rows if r["answer"] == "Yes"]
    no = [r for r in rows if r["answer"] == "No"]
    visible = {"yes": yes, "no": no}.get(show, rows)

    return render_template(
        "admin.html", rows=visible, show=show,
        total=len(rows), yes_count=len(yes), no_count=len(no), party=PARTY,
    )


@app.route("/admin/delete/<int:response_id>", methods=["POST"])
@admin_required
def delete_response(response_id):
    remove_response(response_id)
    flash("RSVP entry deleted.", "success")
    return redirect(url_for("admin", show=request.args.get("show", "all")))


init_db()

if __name__ == "__main__":
    # debug=True is convenient locally; use gunicorn in production.
    app.run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
