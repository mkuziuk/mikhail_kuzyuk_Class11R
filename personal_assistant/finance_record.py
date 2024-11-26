import json
import csv
import uuid
from typing import List, Optional


class FinanceRecord:
    def __init__(
        self, amount: float, category: str, date: str, description: str
    ) -> None:
        self.id = uuid.uuid4()
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self) -> dict:
        """Преобразование объекта FinanceRecord в словарь для сериализации."""
        return {
            "id": str(self.id),
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "description": self.description,
        }


class FinanceService:
    def __init__(self) -> None:
        self.records: List[FinanceRecord] = []

    def add_record(self, record: FinanceRecord) -> None:
        """Добавление новой финансовой записи."""
        self.records.append(record)

    def view_records(self) -> List[FinanceRecord]:
        """Просмотр всех записей."""
        return self.records

    def filter_records(
        self, category: Optional[str] = None, date: Optional[str] = None
    ) -> List[FinanceRecord]:
        """Фильтрация записей по категории или дате."""
        filtered_records = self.records
        if category is not None:
            filtered_records = [
                record for record in filtered_records if record.category == category
            ]

        if date is not None:
            filtered_records = [
                record for record in filtered_records if record.date == date
            ]

        return filtered_records

    def export_to_csv(self, filename: str) -> None:
        """Экспорт финансовых записей в CSV файл."""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Id", "Amount", "Category", "Date", "Description"])
            for record in self.records:
                writer.writerow(
                    [
                        str(record.id),
                        record.amount,
                        record.category,
                        record.date,
                        record.description,
                    ]
                )

    def import_from_csv(self, filename: str) -> None:
        """Импорт финансовых записей из CSV файла."""
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) < 5:
                    continue
                id_str, amount_str, category, date_str, description = row
                amount = float(amount_str)
                record = FinanceRecord(
                    amount=amount,
                    category=category,
                    date=date_str.strip(),
                    description=description,
                )
                self.add_record(record)

    def save_to_json(self, filename: str = "finance.json") -> None:
        """Сохранение финансовых записей в JSON файл."""
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(
                [record.to_dict() for record in self.records],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def load_from_json(self, filename: str = "finance.json") -> None:
        """Загрузка финансовых записей из JSON файла."""
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                records_data = json.load(file)
                for data in records_data:
                    record = FinanceRecord(
                        amount=data["amount"],
                        category=data["category"],
                        date=data["date"],
                        description=data["description"],
                    )
                    self.add_record(record)
        except FileNotFoundError:
            pass


class FinanceController:
    def __init__(self, finance_service: FinanceService) -> None:
        self.finance_service = finance_service

    def handle_choice(self):
        while True:
            print(
                """
1. Добавить финансовую запись
2. Просмотреть все записи
3. Найти запись по ID
4. Редактировать запись
5. Удалить запись
6. Экспортировать записи в CSV
7. Импортировать записи из CSV
8. Сохранить записи в JSON
9. Загрузить записи из JSON
0. Выход
"""
            )
            choice = input("Выберите действие: ")
            if choice == "1":
                amount = float(
                    input(
                        "Сумма (положительное число для доходов, отрицательное для расходов): "
                    )
                )
                category = input("Категория: ")
                date = input("Дата (ДД-ММ-ГГГГ): ")
                description = input("Описание: ")

                record = FinanceRecord(amount, category, date, description)
                self.finance_service.add_record(record)
                print("Финансовая запись добавлена.")

            elif choice == "2":
                records = self.finance_service.view_records()
                if not records:
                    print("Нет доступных записей.")
                else:
                    for record in records:
                        print(
                            f"ID: {record.id}, Сумма: {record.amount}, Категория: {record.category}, "
                            f"Дата: {record.date}, Описание: {record.description}"
                        )

            elif choice == "3":
                record_id = input("Введите ID записи: ")
                record = self.finance_service.get_record_by_id(uuid.UUID(record_id))
                if record:
                    print(
                        f"Запись найдена: Сумма: {record.amount}, Категория: {record.category}, "
                        f"Дата: {record.date}, Описание: {record.description}"
                    )
                else:
                    print("Запись не найдена.")

            elif choice == "4":
                record_id = input("Введите ID записи для редактирования: ")
                record = self.finance_service.get_record_by_id(uuid.UUID(record_id))

                if not record:
                    print("Запись не найдена.")
                    continue

                amount_input = input(f"Новая сумма (текущая: {record.amount}): ")
                amount = float(amount_input) if amount_input else record.amount
                category = (
                    input(f"Новая категория (текущая: {record.category}): ")
                    or record.category
                )
                date = input(f"Новая дата (текущая: {record.date}): ") or record.date
                description = (
                    input(f"Новое описание (текущее: {record.description}): ")
                    or record.description
                )

                new_record = FinanceRecord(amount, category, date, description)
                self.finance_service.replace_record_by_id(record.id, new_record)
                print("Запись обновлена.")

            elif choice == "5":
                record_id = input("Введите ID записи для удаления: ")

                if self.finance_service.delete_record_by_id(uuid.UUID(record_id)):
                    print("Запись удалена.")
                else:
                    print("Запись не найдена.")

            elif choice == "6":
                file_name = (
                    input("Введите имя файла для экспорта (по умолчанию finance.csv): ")
                    or "finance.csv"
                )

                self.finance_service.export_to_csv(file_name)
                print(f"Записи экспортированы в файл {file_name}.")

            elif choice == "7":
                file_name = (
                    input("Введите имя файла для импорта (по умолчанию finance.csv): ")
                    or "finance.csv"
                )

                self.finance_service.import_from_csv(file_name)
                print(f"Записи импортированы из файла {file_name}.")

            elif choice == "8":
                file_name = (
                    input(
                        "Введите имя файла для сохранения (по умолчанию finance.json): "
                    )
                    or "finance.json"
                )

                self.finance_service.save_to_json(file_name)
                print(f"Записи сохранены в файл {file_name}.")

            elif choice == "9":
                file_name = (
                    input(
                        "Введите имя файла для загрузки (по умолчанию finance.json): "
                    )
                    or "finance.json"
                )

                self.finance_service.load_from_json(file_name)
                print(f"Записи загружены из файла {file_name}.")

            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Некорректный выбор, попробуйте снова.")