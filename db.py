from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _to_int_bool(value: bool) -> int:
    return 1 if value else 0


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS dealers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dealer_name TEXT NOT NULL,
                dealer_code TEXT NOT NULL UNIQUE,
                is_on_leave INTEGER NOT NULL DEFAULT 0,
                single_transaction_limit REAL NOT NULL,
                daily_limit REAL,
                yearly_limit REAL,
                primary_user INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        connection.commit()


def seed_dealers() -> None:
    with get_connection() as connection:
        count = connection.execute("SELECT COUNT(1) FROM dealers").fetchone()[0]
        if count == 0:
            connection.executemany(
                """
                INSERT INTO dealers (
                    dealer_name,
                    dealer_code,
                    is_on_leave,
                    single_transaction_limit,
                    daily_limit,
                    yearly_limit,
                    primary_user
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    ("Dealer One", "D001", 0, 50000, 250000, 2500000, 1),
                    ("Dealer Two", "D002", 0, 100000, 500000, 5000000, 1),
                ],
            )
            connection.commit()


def get_dealer_by_code(dealer_code: str) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM dealers WHERE dealer_code = ?",
            (dealer_code,),
        ).fetchone()
        return dict(row) if row else None


def get_dealer_by_id(dealer_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM dealers WHERE id = ?",
            (dealer_id,),
        ).fetchone()
        return dict(row) if row else None


def list_dealers() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                dealer_name,
                dealer_code,
                is_on_leave,
                single_transaction_limit,
                daily_limit,
                yearly_limit,
                primary_user
            FROM dealers
            ORDER BY dealer_name ASC, id ASC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def add_dealer(
    dealer_name: str,
    dealer_code: str,
    is_on_leave: bool,
    single_transaction_limit: float,
    daily_limit: float,
    yearly_limit: float,
    primary_user: bool,
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO dealers (
                dealer_name,
                dealer_code,
                is_on_leave,
                single_transaction_limit,
                daily_limit,
                yearly_limit,
                primary_user
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dealer_name.strip(),
                dealer_code.strip(),
                _to_int_bool(is_on_leave),
                float(single_transaction_limit),
                float(daily_limit),
                float(yearly_limit),
                _to_int_bool(primary_user),
            ),
        )
        connection.commit()


def update_dealer(
    dealer_id: int,
    dealer_name: str,
    dealer_code: str,
    is_on_leave: bool,
    single_transaction_limit: float,
    daily_limit: float,
    yearly_limit: float,
    primary_user: bool,
) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE dealers
            SET
                dealer_name = ?,
                dealer_code = ?,
                is_on_leave = ?,
                single_transaction_limit = ?,
                daily_limit = ?,
                yearly_limit = ?,
                primary_user = ?
            WHERE id = ?
            """,
            (
                dealer_name.strip(),
                dealer_code.strip(),
                _to_int_bool(is_on_leave),
                float(single_transaction_limit),
                float(daily_limit),
                float(yearly_limit),
                _to_int_bool(primary_user),
                dealer_id,
            ),
        )
        connection.commit()


def delete_dealer(dealer_id: int) -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM dealers WHERE id = ?", (dealer_id,))
        connection.commit()
