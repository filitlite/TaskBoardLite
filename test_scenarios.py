"""Manual integration scenarios for TaskBoardLite.

Scenario 1:
1. Start the application.
2. Add task "Проверить поставку" with place "Склад A".
3. Close and open the application again.
4. Check that the task is still visible in the table.

Expected result: the task is loaded from taskboard_lite.db.

Scenario 2:
1. Leave the title field empty.
2. Fill only the place field.
3. Click "Добавить".

Expected result: the application shows a validation warning.

Scenario 3:
1. Add tasks for "Зона 1" and "Зона 2".
2. Type "Зона 2" into search.
3. Check the table.

Expected result: only matching tasks are displayed.

Scenario 4:
1. Select a task in the table.
2. Click "Отметить готово".

Expected result: the selected task status changes to "Готово".
"""
