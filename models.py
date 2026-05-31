"""Data models for TaskBoardLite."""

from dataclasses import dataclass


@dataclass
class Task:
    """Warehouse task or request."""

    title: str
    place: str
    priority: str = "Средний"
    status: str = "Новая"
    task_id: int | None = None

    def short_row(self):
        """Return a tuple suitable for table output."""
        return (
            self.task_id if self.task_id is not None else "",
            self.title,
            self.place,
            self.priority,
            self.status,
        )
