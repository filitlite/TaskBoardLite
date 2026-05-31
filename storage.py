"""SQLite storage layer for TaskBoardLite."""

import sqlite3
from pathlib import Path

from models import Task


class TaskStorage:
    """Stores tasks in a local SQLite database."""

    def __init__(self, database_path="taskboard_lite.db"):
        self.database_path = Path(database_path)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _create_table(self):
        connection = self._connect()
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    place TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()
        finally:
            connection.close()

    def add_task(self, task):
        """Insert a task and return it with an id."""
        connection = self._connect()
        try:
            cursor = connection.execute(
                """
                INSERT INTO tasks (title, place, priority, status)
                VALUES (?, ?, ?, ?)
                """,
                (task.title, task.place, task.priority, task.status),
            )
            task.task_id = cursor.lastrowid
            connection.commit()
            return task
        finally:
            connection.close()

    def update_status(self, task_id, status):
        """Change task status."""
        connection = self._connect()
        try:
            connection.execute(
                "UPDATE tasks SET status = ? WHERE id = ?",
                (status, task_id),
            )
            connection.commit()
        finally:
            connection.close()

    def delete_task(self, task_id):
        """Delete task by id."""
        connection = self._connect()
        try:
            connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            connection.commit()
        finally:
            connection.close()

    def load_tasks(self, search_text=""):
        """Load all tasks or tasks filtered by title/place."""
        connection = self._connect()
        try:
            rows = connection.execute(
                """
                SELECT id, title, place, priority, status
                FROM tasks
                ORDER BY id DESC
                """
            ).fetchall()
        finally:
            connection.close()

        tasks = [
            Task(
                task_id=row[0],
                title=row[1],
                place=row[2],
                priority=row[3],
                status=row[4],
            )
            for row in rows
        ]
        query = search_text.lower()
        if not query:
            return tasks
        return [
            task for task in tasks
            if query in task.title.lower() or query in task.place.lower()
        ]
