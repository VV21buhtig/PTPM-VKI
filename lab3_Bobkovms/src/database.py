"""Класс работы с БД (п. b): SQLite, методы add/get/delete."""

import sqlite3


class TriangleDatabase:
    """Одна запись: длина1, длина2, длина3, тип_треугольника, сообщение_об_ошибке.

    Запись идентифицируется тройкой исходных строк длин сторон.
    """

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS triangles (
                side_a TEXT NOT NULL,
                side_b TEXT NOT NULL,
                side_c TEXT NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT,
                PRIMARY KEY (side_a, side_b, side_c)
            )
            """
        )
        self.conn.commit()

    @staticmethod
    def _key(a, b, c) -> tuple:
        return (str(a).strip(), str(b).strip(), str(c).strip())

    def add_record(self, side_a, side_b, side_c, triangle_type: str, error_message=None) -> None:
        key = self._key(side_a, side_b, side_c)
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles (side_a, side_b, side_c, triangle_type, error_message)"
            " VALUES (?, ?, ?, ?, ?)",
            (*key, triangle_type, error_message),
        )
        self.conn.commit()

    def get_record(self, side_a, side_b, side_c):
        key = self._key(side_a, side_b, side_c)
        cur = self.conn.execute(
            "SELECT side_a, side_b, side_c, triangle_type, error_message FROM triangles"
            " WHERE side_a = ? AND side_b = ? AND side_c = ?",
            key,
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {
            "side_a": row[0],
            "side_b": row[1],
            "side_c": row[2],
            "triangle_type": row[3],
            "error_message": row[4],
        }

    def delete_record(self, side_a, side_b, side_c) -> bool:
        key = self._key(side_a, side_b, side_c)
        cur = self.conn.execute(
            "DELETE FROM triangles WHERE side_a = ? AND side_b = ? AND side_c = ?",
            key,
        )
        self.conn.commit()
        return cur.rowcount > 0

    def close(self) -> None:
        self.conn.close()
