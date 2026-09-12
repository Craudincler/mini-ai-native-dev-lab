from pathlib import Path
import sqlite3

DB_PATH = Path("/data/lab.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        count = connection.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        if count == 0:
            connection.executemany(
                """
                INSERT INTO projects (name, category, status)
                VALUES (?, ?, ?)
                """,
                [
                    ("Portal da Associação Comunitária", "Comunidade", "Planejamento"),
                    ("Painel de Ações da ONG", "ONG", "Preparação"),
                    ("Agenda Digital da Escola", "Educação", "Estrutura inicial"),
                ],
            )
        connection.commit()


def list_projects():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, name, category, status FROM projects ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
