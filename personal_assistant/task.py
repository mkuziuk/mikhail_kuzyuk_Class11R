import uuid
import csv
import json
from typing import List, Optional


class Task:
    def __init__(
        self, title: str, description: str, done: bool, priority: int, due_date: str
    ) -> None:
        self.id = uuid.uuid4()
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date,
        }


class TaskService:
    def __init__(self, tasks: Optional[List[Task]] = None) -> None:
        self.tasks = tasks if tasks is not None else []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    def get_task_by_id(self, id: uuid.UUID) -> Optional[Task]:
        for task in self.tasks:
            if task.id == id:
                return task
        return None

    def replace_task_by_id(self, id: uuid.UUID, new_task: Task) -> None:
        for i, task in enumerate(self.tasks):
            if task.id == id:
                self.tasks[i] = new_task
                break

    def delete_task_by_id(self, id: uuid.UUID) -> None:
        for i, task in enumerate(self.tasks):
            if task.id == id:
                self.tasks.pop(i)
                break

    def export_as_csv(self, filename: str) -> None:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Id", "Title", "Description", "Done", "Priority", "Due_date"]
            )
            for task in self.tasks:
                writer.writerow(
                    [
                        str(task.id),
                        task.title,
                        task.description,
                        task.done,
                        task.priority,
                        task.due_date,
                    ]
                )

    def import_csv(self, filename: str) -> None:
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) < 6:
                    continue
                id_str, title, description, done_str, priority_str, due_date = row
                done = done_str.lower() == "true"
                priority = int(priority_str)
                task = Task(
                    title=title,
                    description=description,
                    done=done,
                    priority=priority,
                    due_date=due_date,
                )
                self.add_task(task)

    def save_to_json(self, filename: str) -> None:
        """Save tasks to a JSON file."""
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(
                [task.to_dict() for task in self.tasks],
                file,
                ensure_ascii=False,
                indent=4,
            )


class TaskController:
    def __init__(self, task_service: TaskService) -> None:
        self.task_service = task_service

    def handle_choice(self):
        while True:
            print(
                """
1. Добавить задачу
2. Просмотреть все задачи
3. Найти задачу по ID
4. Редактировать задачу
5. Удалить задачу
6. Экспортировать задачи в CSV
7. Импортировать задачи из CSV
8. Сохранить задачи в JSON
9. Загрузить задачи из JSON
0. Выход
"""
            )
            choice = input("Выберите действие: ")
            if choice == "1":
                title = input("Название задачи: ")
                description = input("Описание задачи: ")
                done = input("Статус (True/False): ").lower() == "true"
                priority = int(input("Приоритет: "))
                due_date = input("Срок выполнения (ДД-ММ-ГГГГ): ")

                task = Task(title, description, done, priority, due_date)
                self.task_service.add_task(task)
                print("Задача добавлена.")

            elif choice == "2":
                tasks = self.task_service.get_all_tasks()
                if not tasks:
                    print("Нет доступных задач.")
                else:
                    for task in tasks:
                        print(
                            f"ID: {task.id}, Название: {task.title}, Описание: {task.description}, "
                            f"Статус: {task.done}, Приоритет: {task.priority}, Срок: {task.due_date}"
                        )

            elif choice == "3":
                task_id = input("Введите ID задачи: ")
                task = self.task_service.get_task_by_id(uuid.UUID(task_id))
                if task:
                    print(
                        f"Задача найдена: Название: {task.title}, Описание: {task.description}, "
                        f"Статус: {task.done}, Приоритет: {task.priority}, Срок: {task.due_date}"
                    )
                else:
                    print("Задача не найдена.")

            elif choice == "4":
                task_id = input("Введите ID задачи для редактирования: ")
                task = self.task_service.get_task_by_id(uuid.UUID(task_id))

                if not task:
                    print("Задача не найдена.")
                    continue

                title = input(f"Новое название (текущее: {task.title}): ") or task.title
                description = (
                    input(f"Новое описание (текущее: {task.description}): ")
                    or task.description
                )
                done_input = input(f"Новый статус (текущее: {task.done}): ")
                done = done_input.lower() == "true" if done_input else task.done
                priority_input = input(f"Новый приоритет (текущий: {task.priority}): ")
                priority = int(priority_input) if priority_input else task.priority
                due_date = (
                    input(f"Новый срок (текущий: {task.due_date}): ") or task.due_date
                )

                new_task = Task(title, description, done, priority, due_date)
                self.task_service.replace_task_by_id(task.id, new_task)
                print("Задача обновлена.")

            elif choice == "5":
                task_id = input("Введите ID задачи для удаления: ")

                if self.task_service.delete_task_by_id(uuid.UUID(task_id)):
                    print("Задача удалена.")
                else:
                    print("Задача не найдена.")

            elif choice == "6":
                file_name = (
                    input("Введите имя файла для экспорта (по умолчанию tasks.csv): ")
                    or "tasks.csv"
                )

                self.task_service.export_as_csv(file_name)
                print(f"Задачи экспортированы в файл {file_name}.")

            elif choice == "7":
                file_name = (
                    input("Введите имя файла для импорта (по умолчанию tasks.csv): ")
                    or "tasks.csv"
                )

                self.task_service.import_csv(file_name)
                print(f"Задачи импортированы из файла {file_name}.")

            elif choice == "8":
                file_name = (
                    input(
                        "Введите имя файла для сохранения (по умолчанию tasks.json): "
                    )
                    or "tasks.json"
                )

                self.task_service.save_to_json(file_name)
                print(f"Задачи сохранены в файл {file_name}.")

            elif choice == "9":
                file_name = (
                    input("Введите имя файла для загрузки (по умолчанию tasks.json): ")
                    or "tasks.json"
                )

                self.task_service.load_from_json(file_name)
                print(f"Задачи загружены из файла {file_name}.")

            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Некорректный выбор, попробуйте снова.")
