"""Tests for TaskBoardLite storage."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from models import Task
from storage import TaskStorage


class TaskStorageTest(TestCase):
    """Checks SQLite operations."""

    def test_add_and_load_task(self):
        with TemporaryDirectory() as tmp_dir:
            storage = TaskStorage(Path(tmp_dir) / "tasks.db")

            storage.add_task(Task("Проверить поставку", "Склад A", "Высокий"))
            tasks = storage.load_tasks()

            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0].title, "Проверить поставку")
            self.assertEqual(tasks[0].priority, "Высокий")

    def test_search_by_place(self):
        with TemporaryDirectory() as tmp_dir:
            storage = TaskStorage(Path(tmp_dir) / "tasks.db")

            storage.add_task(Task("Проверить коробки", "Зона 1"))
            storage.add_task(Task("Принять товар", "Зона 2"))
            tasks = storage.load_tasks("зона 2")

            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0].title, "Принять товар")

    def test_update_status_and_delete(self):
        with TemporaryDirectory() as tmp_dir:
            storage = TaskStorage(Path(tmp_dir) / "tasks.db")

            task = storage.add_task(Task("Собрать заказ", "Стеллаж 4"))
            storage.update_status(task.task_id, "Готово")
            self.assertEqual(storage.load_tasks()[0].status, "Готово")

            storage.delete_task(task.task_id)
            self.assertEqual(storage.load_tasks(), [])


if __name__ == "__main__":
    main()
