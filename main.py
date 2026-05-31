"""TaskBoardLite desktop application."""

import tkinter as tk
from tkinter import messagebox, ttk

from models import Task
from storage import TaskStorage


class TaskBoardApp(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.title("TaskBoardLite")
        self.geometry("980x620")
        self.minsize(860, 540)
        self.configure(bg="#eef3f7")

        self.storage = TaskStorage()
        self.selected_task_id = None

        self.title_var = tk.StringVar()
        self.place_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Средний")
        self.status_var = tk.StringVar(value="Новая")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_tasks())

        self._build_styles()
        self._build_layout()
        self.refresh_tasks()

    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=34, font=("Segoe UI", 10))
        style.configure(
            "Treeview.Heading",
            background="#d8e6f1",
            foreground="#1d2a35",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", "#b7d7ef")])

    def _build_layout(self):
        header = tk.Frame(self, bg="#22313f", height=78)
        header.pack(fill="x")
        tk.Label(
            header,
            text="TaskBoardLite",
            bg="#22313f",
            fg="white",
            font=("Segoe UI", 24, "bold"),
        ).pack(side="left", padx=28)
        tk.Label(
            header,
            text="учет складских задач и заявок",
            bg="#22313f",
            fg="#c7d4df",
            font=("Segoe UI", 12),
        ).pack(side="left", pady=8)

        workspace = tk.Frame(self, bg="#eef3f7")
        workspace.pack(fill="both", expand=True, padx=24, pady=22)

        form = tk.Frame(workspace, bg="#ffffff", bd=0, highlightthickness=1,
                        highlightbackground="#d5dee6")
        form.pack(side="left", fill="y", padx=(0, 18))

        tk.Label(
            form,
            text="Новая заявка",
            bg="#ffffff",
            fg="#1d2a35",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 10))

        self._entry(form, "Название", self.title_var)
        self._entry(form, "Зона / место", self.place_var)
        self._combo(form, "Приоритет", self.priority_var,
                    ["Низкий", "Средний", "Высокий"])
        self._combo(form, "Статус", self.status_var,
                    ["Новая", "В работе", "Готово"])

        tk.Button(
            form,
            text="Добавить",
            command=self.add_task,
            bg="#1d7a8c",
            fg="white",
            activebackground="#145866",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            height=2,
        ).pack(fill="x", padx=18, pady=(16, 8))
        tk.Button(
            form,
            text="Удалить выбранную",
            command=self.delete_selected,
            bg="#d95f59",
            fg="white",
            activebackground="#ad403b",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            height=2,
        ).pack(fill="x", padx=18, pady=8)
        tk.Button(
            form,
            text="Отметить готово",
            command=self.mark_done,
            bg="#6d7784",
            fg="white",
            activebackground="#4f5863",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            height=2,
        ).pack(fill="x", padx=18, pady=8)

        content = tk.Frame(workspace, bg="#eef3f7")
        content.pack(side="left", fill="both", expand=True)

        search_row = tk.Frame(content, bg="#eef3f7")
        search_row.pack(fill="x", pady=(0, 12))
        tk.Label(
            search_row,
            text="Поиск",
            bg="#eef3f7",
            fg="#1d2a35",
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")
        tk.Entry(
            search_row,
            textvariable=self.search_var,
            bg="white",
            fg="#1d2a35",
            relief="flat",
            font=("Segoe UI", 11),
            highlightthickness=1,
            highlightbackground="#c8d3dd",
        ).pack(side="left", fill="x", expand=True, padx=12, ipady=8)

        columns = ("id", "title", "place", "priority", "status")
        self.table = ttk.Treeview(content, columns=columns, show="headings")
        self.table.heading("id", text="ID")
        self.table.heading("title", text="Заявка")
        self.table.heading("place", text="Место")
        self.table.heading("priority", text="Приоритет")
        self.table.heading("status", text="Статус")
        self.table.column("id", width=60, anchor="center")
        self.table.column("title", width=330)
        self.table.column("place", width=180)
        self.table.column("priority", width=120, anchor="center")
        self.table.column("status", width=120, anchor="center")
        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.on_select)

    def _entry(self, parent, label, variable):
        tk.Label(
            parent,
            text=label,
            bg="#ffffff",
            fg="#485866",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=18, pady=(10, 4))
        tk.Entry(
            parent,
            textvariable=variable,
            bg="#f7fafc",
            fg="#1d2a35",
            relief="flat",
            font=("Segoe UI", 11),
            highlightthickness=1,
            highlightbackground="#d5dee6",
        ).pack(fill="x", padx=18, ipady=8)

    def _combo(self, parent, label, variable, values):
        tk.Label(
            parent,
            text=label,
            bg="#ffffff",
            fg="#485866",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=18, pady=(10, 4))
        ttk.Combobox(
            parent,
            textvariable=variable,
            values=values,
            state="readonly",
            font=("Segoe UI", 10),
        ).pack(fill="x", padx=18, ipady=4)

    def add_task(self):
        title = self.title_var.get().strip()
        place = self.place_var.get().strip()
        if not title or not place:
            messagebox.showwarning("Проверка", "Заполните название и место.")
            return

        self.storage.add_task(
            Task(
                title=title,
                place=place,
                priority=self.priority_var.get(),
                status=self.status_var.get(),
            )
        )
        self.title_var.set("")
        self.place_var.set("")
        self.priority_var.set("Средний")
        self.status_var.set("Новая")
        self.refresh_tasks()

    def refresh_tasks(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for task in self.storage.load_tasks(self.search_var.get().strip()):
            self.table.insert("", "end", values=task.short_row())

    def on_select(self, _event):
        selected = self.table.selection()
        if not selected:
            self.selected_task_id = None
            return
        values = self.table.item(selected[0], "values")
        self.selected_task_id = int(values[0])

    def delete_selected(self):
        if self.selected_task_id is None:
            messagebox.showinfo("Удаление", "Выберите заявку в таблице.")
            return
        self.storage.delete_task(self.selected_task_id)
        self.selected_task_id = None
        self.refresh_tasks()

    def mark_done(self):
        if self.selected_task_id is None:
            messagebox.showinfo("Статус", "Выберите заявку в таблице.")
            return
        self.storage.update_status(self.selected_task_id, "Готово")
        self.refresh_tasks()


if __name__ == "__main__":
    TaskBoardApp().mainloop()
