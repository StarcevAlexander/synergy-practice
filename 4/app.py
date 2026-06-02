"""
Кейс-задача № 4. WEB-приложение архитектуры «клиент — сервер — БД».

В задании предлагается стек Delphi 10.2 + IIS + MS SQL Server. Поскольку
Delphi/IIS — проприетарная среда Windows, для воспроизводимости и кроссплатформенного
запуска реализован эквивалентный по архитектуре WEB-проект на Python (Flask):

    Браузер (HTTP)  ──>  WEB-сервер приложения (Flask/WSGI)  ──>  БД (SQLite/MS SQL Server)

Архитектура полностью соответствует трёхзвенной WEB-архитектуре, описанной в ANALYSIS.md.
SQL-схема для MS SQL Server приложена в файле schema_mssql.sql.

Тема приложения — каталог и заявки на туры («Турагентство»).
"""

import os
import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tourism.db")

app = Flask(__name__)


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    """Создаёт таблицы и наполняет демо-данными (для SQLite)."""
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS tours (
            tour_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT    NOT NULL,
            country   TEXT    NOT NULL,
            nights    INTEGER NOT NULL,
            price     REAL    NOT NULL
        );
        CREATE TABLE IF NOT EXISTS requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tour_id    INTEGER NOT NULL REFERENCES tours(tour_id),
            client     TEXT    NOT NULL,
            phone      TEXT    NOT NULL,
            persons    INTEGER NOT NULL,
            created_at TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        """
    )
    if db.execute("SELECT COUNT(*) FROM tours").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO tours (title, country, nights, price) VALUES (?,?,?,?)",
            [
                ("Турция всё включено", "Турция", 7, 45000),
                ("Выходные в Риме", "Италия", 3, 60000),
                ("Пляжный Пхукет", "Таиланд", 10, 85000),
            ],
        )
    db.commit()
    db.close()


@app.route("/")
def index():
    tours = get_db().execute("SELECT * FROM tours ORDER BY price").fetchall()
    return render_template("index.html", tours=tours)


@app.route("/tour/<int:tour_id>")
def tour(tour_id: int):
    row = get_db().execute("SELECT * FROM tours WHERE tour_id = ?", (tour_id,)).fetchone()
    if row is None:
        return "Тур не найден", 404
    return render_template("tour.html", tour=row)


@app.route("/tour/<int:tour_id>/order", methods=["POST"])
def make_order(tour_id: int):
    db = get_db()
    db.execute(
        "INSERT INTO requests (tour_id, client, phone, persons) VALUES (?,?,?,?)",
        (
            tour_id,
            request.form["client"],
            request.form["phone"],
            int(request.form["persons"]),
        ),
    )
    db.commit()
    return redirect(url_for("requests_list"))


@app.route("/requests")
def requests_list():
    rows = get_db().execute(
        """
        SELECT r.request_id, t.title, r.client, r.phone, r.persons, r.created_at
        FROM requests r JOIN tours t ON t.tour_id = r.tour_id
        ORDER BY r.created_at DESC
        """
    ).fetchall()
    return render_template("requests.html", requests=rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
