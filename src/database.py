import sqlite3
from typing import Optional, List, Dict, Any


class DatabaseRepository:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        );
        """
        with self.conn:
            self.conn.execute(query)

    def _validate_id(self, comment_id: int) -> None:
        if not isinstance(comment_id, int) or isinstance(comment_id, bool):
            raise TypeError("ID сообщения должен быть целым числом (int)")

    def _validate_name(self, username: str) -> None:
        if not isinstance(username, str):
            raise TypeError("Имя пользователя должно быть строкой (str)")
        if not username.strip() or len(username) > 256:
            raise ValueError("Имя пользователя не может быть пустым и превышать 256 символов")

    def _validate_message(self, message: str) -> None:
        if not isinstance(message, str):
            raise TypeError("Текст сообщения должен быть строкой (str)")
        if not message.strip() or len(message) > 8096:
            raise ValueError("Текст сообщения не может быть пустым и превышать 8096 символов")

    def add(self, comment_id: int, username: str, message: str) -> bool:
        self._validate_id(comment_id)
        self._validate_name(username)
        self._validate_message(message)

        query = "INSERT INTO comments (id, name, message) VALUES (?, ?, ?);"
        with self.conn:
            self.conn.execute(query, (comment_id, username, message))
        return True

    def get_by_id(self, comment_id: int) -> Optional[Dict[str, Any]]:
        self._validate_id(comment_id)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, message FROM comments WHERE id = ?;", (comment_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str) -> List[Dict[str, Any]]:
        self._validate_name(username)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, message FROM comments WHERE name = ?;", (username,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def update(self, comment_id: int, new_message: str) -> bool:
        self._validate_id(comment_id)
        self._validate_message(new_message)

        with self.conn:
            cursor = self.conn.execute(
                "UPDATE comments SET message = ? WHERE id = ?;",
                (new_message, comment_id)
            )
            if cursor.rowcount == 0:
                raise KeyError(f"Запись с ID {comment_id} не найдена")
        return True

    def delete(self, comment_id: int) -> bool:
        self._validate_id(comment_id)

        with self.conn:
            cursor = self.conn.execute("DELETE FROM comments WHERE id = ?;", (comment_id,))
            if cursor.rowcount == 0:
                raise KeyError(f"Запись с ID {comment_id} не найдена")
        return True

    def close(self) -> None:
        self.conn.close()
