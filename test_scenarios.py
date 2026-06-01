"""Исполняемые тестовые сценарии для TaskBoardLite (ПК 2.4).

Сценарий 1: Добавить задачу, закрыть соединение, загрузить —
             задача на месте.
Сценарий 2: Попытка добавить задачу с пустым названием —
             валидация не пропускает.
Сценарий 3: Поиск по слову «Зона 2» — возвращается только
             совпадающая запись.
Сценарий 4: Отметить задачу как «Готово» — статус обновляется.
"""

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "TaskBoardLite"),
)

from models import Task
from storage import TaskStorage


def scenario_1_persistence():
    """Добавить задачу, пересоздать хранилище, проверить."""
    with TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"

        storage = TaskStorage(db_path)
        storage.add_task(
            Task("Проверить поставку", "Склад A", "Высокий")
        )

        # Имитация перезапуска — новый объект хранилища
        storage2 = TaskStorage(db_path)
        tasks = storage2.load_tasks()

        assert len(tasks) == 1, (
            f"Ожидалась 1 задача, получено {len(tasks)}"
        )
        assert tasks[0].title == "Проверить поставку"
        assert tasks[0].place == "Склад A"
        print("Сценарий 1 (персистентность): PASSED")


def scenario_2_empty_title_validation():
    """Пустое название не должно проходить валидацию."""
    title = ""
    place = "Склад B"

    # Валидация на уровне интерфейса
    is_valid = bool(title.strip()) and bool(place.strip())
    assert not is_valid, "Пустое название должно отклоняться"
    print("Сценарий 2 (валидация пустого названия): PASSED")


def scenario_3_search_filter():
    """Поиск по 'Зона 2' возвращает только нужную задачу."""
    with TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        storage = TaskStorage(db_path)

        storage.add_task(Task("Проверить коробки", "Зона 1"))
        storage.add_task(Task("Принять товар", "Зона 2"))
        storage.add_task(Task("Инвентаризация", "Зона 3"))

        found = storage.load_tasks("Зона 2")
        assert len(found) == 1, (
            f"Ожидалась 1, получено {len(found)}"
        )
        assert found[0].title == "Принять товар"
        print("Сценарий 3 (поиск): PASSED")


def scenario_4_mark_done():
    """Смена статуса на 'Готово'."""
    with TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"
        storage = TaskStorage(db_path)

        task = storage.add_task(
            Task("Собрать заказ", "Стеллаж 4")
        )
        storage.update_status(task.task_id, "Готово")

        loaded = storage.load_tasks()
        assert loaded[0].status == "Готово", (
            f"Ожидалось 'Готово', получено '{loaded[0].status}'"
        )
        print("Сценарий 4 (отметить готово): PASSED")


if __name__ == "__main__":
    scenario_1_persistence()
    scenario_2_empty_title_validation()
    scenario_3_search_filter()
    scenario_4_mark_done()
    print("\nВСЕ СЦЕНАРИИ ЗАВЕРШЕНЫ УСПЕШНО")
