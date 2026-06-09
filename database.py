import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent / "series.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS series (
                titulo TEXT PRIMARY KEY,
                genero TEXT,
                ano_lancamento INTEGER,
                temporadas INTEGER
            )
            """
        )
        connection.commit()


def upsert_serie(
    titulo: str, genero: str, ano_lancamento: int, temporadas: int
) -> None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO series (titulo, genero, ano_lancamento, temporadas)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(titulo) DO UPDATE SET
                genero = excluded.genero,
                ano_lancamento = excluded.ano_lancamento,
                temporadas = excluded.temporadas
            """,
            (titulo, genero, ano_lancamento, temporadas),
        )
        connection.commit()


def find_serie_by_title(title: str) -> Optional[dict]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT titulo, genero, ano_lancamento, temporadas "
            "FROM series WHERE LOWER(titulo) = LOWER(?)",
            (title,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)
