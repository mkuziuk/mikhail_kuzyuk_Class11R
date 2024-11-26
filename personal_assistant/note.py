import uuid
import csv
import json
from typing import List, Optional


class Note:
    def __init__(self, title: str, content: str, timestamp: str) -> None:
        self.id = uuid.uuid4()
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp,
        }


class NoteService:
    def __init__(self) -> None:
        self.notes: List[Note] = []

    def add_note(self, note: Note) -> None:
        """Добавление новой заметки."""
        self.notes.append(note)

    def get_all_notes(self) -> List[Note]:
        """Получение всех заметок."""
        return self.notes

    def get_note_by_id(self, id: uuid.UUID) -> Optional[Note]:
        """Получение заметки по ID."""
        for note in self.notes:
            if note.id == id:
                return note
        return None

    def replace_note_by_id(self, id: uuid.UUID, new_note: Note) -> bool:
        """Замена заметки по ID."""
        for i, note in enumerate(self.notes):
            if note.id == id:
                self.notes[i] = new_note
                return True
        return False

    def delete_note_by_id(self, id: uuid.UUID) -> bool:
        """Удаление заметки по ID."""
        for i, note in enumerate(self.notes):
            if note.id == id:
                self.notes.pop(i)
                return True
        return False

    def export_as_csv(self, filename: str = "notes.csv") -> None:
        """Экспорт всех заметок в CSV файл."""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Id", "Title", "Content", "Timestamp"])
            for note in self.notes:
                writer.writerow(
                    [str(note.id), note.title, note.content, note.timestamp]
                )

    def import_csv(self, filename: str = "notes.csv") -> None:
        """Импорт заметок из CSV файла."""
        try:
            with open(filename, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) < 4:
                        continue
                    id_str, title, content, timestamp = row
                    note = Note(title=title, content=content, timestamp=timestamp)
                    self.add_note(note)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

    def export_as_json(self, filename: str = "notes.json") -> None:
        """Сохранение всех заметок в JSON файл."""
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(
                [note.to_dict() for note in self.notes],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def import_json(self, filename: str = "notes.json") -> None:
        """Загрузка заметок из JSON файла."""
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                notes_data = json.load(file)
                for data in notes_data:
                    note = Note(
                        title=data["title"],
                        content=data["content"],
                        timestamp=data["timestamp"],
                    )
                    self.add_note(note)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")


class NoteController:
    def __init__(self, note_service: NoteService) -> None:
        self.note_service = note_service

    def handle_choice(self):
        while True:
            print(
                """
1. Добавить заметку
2. Просмотреть все заметки
3. Найти заметку по ID
4. Редактировать заметку
5. Удалить заметку
6. Экспортировать заметки в CSV
7. Импортировать заметки из CSV
8. Сохранить заметки в JSON
9. Загрузить заметки из JSON
0. Выход
"""
            )
            choice = input("Выберите действие: ")
            if choice == "1":
                title = input("Название: ")
                content = input("Контент: ")
                timestamp = input("Время: ")

                note = Note(title, content, timestamp)
                self.note_service.add_note(note)
                print("Заметка добавлена.")

            elif choice == "2":
                notes = self.note_service.get_all_notes()
                if not notes:
                    print("Нет доступных заметок.")
                else:
                    for note in notes:
                        print(
                            f"ID: {note.id}, Название: {note.title}, Контент: {note.content}, Время: {note.timestamp}"
                        )

            elif choice == "3":
                note_id = input("Введите ID заметки: ")
                note = self.note_service.get_note_by_id(uuid.UUID(note_id))
                if note:
                    print(
                        f"Заметка найдена: Название: {note.title}, Контент: {note.content}, Время: {note.timestamp}"
                    )
                else:
                    print("Заметка не найдена.")

            elif choice == "4":
                note_id = input("Введите ID заметки для редактирования: ")
                note = self.note_service.get_note_by_id(uuid.UUID(note_id))

                if not note:
                    print("Заметка не найдена.")
                    continue

                title = input(f"Новое название (текущее: {note.title}): ") or note.title
                content = (
                    input(f"Новое содержимое (текущее: {note.content}): ")
                    or note.content
                )
                timestamp = (
                    input(f"Новое время (текущее: {note.timestamp}): ")
                    or note.timestamp
                )

                new_note = Note(title, content, timestamp)
                self.note_service.replace_note_by_id(note.id, new_note)
                print("Заметка обновлена.")

            elif choice == "5":
                note_id = input("Введите ID заметки для удаления: ")

                if self.note_service.delete_note_by_id(uuid.UUID(note_id)):
                    print("Заметка удалена.")
                else:
                    print("Заметка не найдена.")

            elif choice == "6":
                file_name = (
                    input("Введите имя файла для экспорта (по умолчанию notes.csv): ")
                    or "notes.csv"
                )

                self.note_service.export_as_csv(file_name)
                print(f"Заметки экспортированы в файл {file_name}.")

            elif choice == "7":
                file_name = (
                    input("Введите имя файла для импорта (по умолчанию notes.csv): ")
                    or "notes.csv"
                )

                self.note_service.import_csv(file_name)
                print(f"Заметки импортированы из файла {file_name}.")

            elif choice == "8":
                file_name = (
                    input(
                        "Введите имя файла для сохранения (по умолчанию notes.json): "
                    )
                    or "notes.json"
                )

                self.note_service.save_to_json(file_name)
                print(f"Заметки сохранены в файл {file_name}.")

            elif choice == "9":
                file_name = (
                    input("Введите имя файла для загрузки (по умолчанию notes.json): ")
                    or "notes.json"
                )

                self.note_service.load_from_json(file_name)
                print(f"Заметки загружены из файла {file_name}.")

            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Некорректный выбор, попробуйте снова.")
