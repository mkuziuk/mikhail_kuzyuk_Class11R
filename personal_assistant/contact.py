import json
import csv
import uuid
from typing import List, Optional


class Contact:
    def __init__(self, name: str, phone: str, email: str) -> None:
        self.id = uuid.uuid4()
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }


class ContactService:
    def __init__(self) -> None:
        self.contacts: List[Contact] = []

    def add_contact(self, contact: Contact) -> None:
        """Добавление нового контакта."""
        self.contacts.append(contact)

    def get_all_contacts(self) -> List[Contact]:
        """Получение всех контактов."""
        return self.contacts

    def find_contact(self, search_term: str) -> List[Contact]:
        """Поиск контакта по имени или номеру телефона."""
        return [
            contact
            for contact in self.contacts
            if search_term.lower() in contact.name.lower()
            or search_term in contact.phone
        ]

    def edit_contact(
        self,
        contact_id: str,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
    ) -> bool:
        """Редактирование контакта."""
        for contact in self.contacts:
            if str(contact.id) == contact_id:
                if name is not None:
                    contact.name = name
                if phone is not None:
                    contact.phone = phone
                if email is not None:
                    contact.email = email
                return True
        return False

    def delete_contact(self, contact_id: str) -> bool:
        """Удаление контакта по ID."""
        for i, contact in enumerate(self.contacts):
            if str(contact.id) == contact_id:
                self.contacts.pop(i)
                return True
        return False

    def export_to_csv(self, filename: str) -> None:
        """Экспорт контактов в CSV файл."""
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Id", "Name", "Phone", "Email"])
            for contact in self.contacts:
                writer.writerow(
                    [str(contact.id), contact.name, contact.phone, contact.email]
                )

    def import_from_csv(self, filename: str) -> None:
        """Импорт контактов из CSV файла."""
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) < 4:
                    continue
                id_str, name, phone, email = row
                contact = Contact(name=name, phone=phone, email=email)
                self.add_contact(contact)

    def save_to_json(self, filename: str = "contacts.json") -> None:
        """Сохранение контактов в JSON файл."""
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(
                [contact.to_dict() for contact in self.contacts],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def load_from_json(self, filename: str = "contacts.json") -> None:
        """Загрузка контактов из JSON файла."""
        try:
            with open(filename, mode="r", encoding="utf-8") as file:
                contacts_data = json.load(file)
                for data in contacts_data:
                    contact = Contact(
                        name=data["name"], phone=data["phone"], email=data["email"]
                    )
                    self.add_contact(contact)
        except FileNotFoundError:
            pass


class ContactController:
    def __init__(self, contact_service: ContactService) -> None:
        self.contact_service = contact_service

    def handle_choice(self):
        while True:
            print(
                """
1. Добавить контакт
2. Просмотреть все контакты
3. Найти контакт по имени или телефону
4. Редактировать контакт
5. Удалить контакт
6. Экспортировать контакты в CSV
7. Импортировать контакты из CSV
8. Сохранить контакты в JSON
9. Загрузить контакты из JSON
0. Выход
"""
            )
            choice = input("Выберите действие: ")
            if choice == "1":
                name = input("Имя: ")
                phone = input("Телефон: ")
                email = input("Электронная почта: ")

                contact = Contact(name=name, phone=phone, email=email)
                self.contact_service.add_contact(contact)
                print("Контакт добавлен.")

            elif choice == "2":
                contacts = self.contact_service.get_all_contacts()
                if not contacts:
                    print("Нет доступных контактов.")
                else:
                    for contact in contacts:
                        print(
                            f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, "
                            f"Электронная почта: {contact.email}"
                        )

            elif choice == "3":
                search_term = input("Введите имя или телефон для поиска: ")
                found_contacts = self.contact_service.find_contact(search_term)
                if not found_contacts:
                    print("Контакты не найдены.")
                else:
                    for contact in found_contacts:
                        print(
                            f"ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, "
                            f"Электронная почта: {contact.email}"
                        )

            elif choice == "4":
                search_term = input(
                    "Введите имя или телефон контакта для редактирования: "
                )
                found_contacts = self.contact_service.find_contact(search_term)

                if not found_contacts:
                    print("Контакты не найдены.")
                    continue

                # Если найдено несколько контактов, показываем их и даем возможность выбрать
                if len(found_contacts) > 1:
                    print("Найдено несколько контактов:")
                    for i, contact in enumerate(found_contacts):
                        print(
                            f"{i + 1}. ID: {contact.id}, Имя: {contact.name}, Телефон: {contact.phone}, "
                            f"Электронная почта: {contact.email}"
                        )
                    index = (
                        int(
                            input(
                                "Выберите номер контакта для редактирования (введите номер): "
                            )
                        )
                        - 1
                    )
                    contact_to_edit = found_contacts[index]
                else:
                    contact_to_edit = found_contacts[0]

                name = (
                    input(f"Новое имя (текущее: {contact_to_edit.name}): ")
                    or contact_to_edit.name
                )
                phone = (
                    input(f"Новый телефон (текущий: {contact_to_edit.phone}): ")
                    or contact_to_edit.phone
                )
                email = (
                    input(
                        f"Новая электронная почта (текущая: {contact_to_edit.email}): "
                    )
                    or contact_to_edit.email
                )

                self.contact_service.edit_contact(
                    str(contact_to_edit.id), name, phone, email
                )
                print("Контакт обновлен.")

            elif choice == "5":
                contact_id = input("Введите ID контакта для удаления: ")

                if self.contact_service.delete_contact(contact_id):
                    print("Контакт удален.")
                else:
                    print("Контакт не найден.")

            elif choice == "6":
                file_name = (
                    input(
                        "Введите имя файла для экспорта (по умолчанию contacts.csv): "
                    )
                    or "contacts.csv"
                )

                self.contact_service.export_to_csv(file_name)
                print(f"Контакты экспортированы в файл {file_name}.")

            elif choice == "7":
                file_name = (
                    input("Введите имя файла для импорта (по умолчанию contacts.csv): ")
                    or "contacts.csv"
                )

                self.contact_service.import_from_csv(file_name)
                print(f"Контакты импортированы из файла {file_name}.")

            elif choice == "8":
                file_name = (
                    input(
                        "Введите имя файла для сохранения (по умолчанию contacts.json): "
                    )
                    or "contacts.json"
                )

                self.contact_service.save_to_json(file_name)
                print(f"Контакты сохранены в файл {file_name}.")

            elif choice == "9":
                file_name = (
                    input(
                        "Введите имя файла для загрузки (по умолчанию contacts.json): "
                    )
                    or "contacts.json"
                )

                self.contact_service.load_from_json(file_name)
                print(f"Контакты загружены из файла {file_name}.")

            elif choice == "0":
                print("Выход из программы.")
                break

            else:
                print("Некорректный выбор, попробуйте снова.")
