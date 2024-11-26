from note import NoteService, NoteController
from task import TaskService, TaskController
from contact import ContactController, ContactService
from finance_record import FinanceController, FinanceService

# from finance_record import FinanceController
# from contact import ContactController

note_service = NoteService()
note_controller = NoteController(note_service)

task_service = TaskService()
task_controller = TaskController(task_service)

contact_service = ContactService()
contact_controller = ContactController(contact_service)

finance_service = FinanceService()
finance_controller = FinanceController(finance_service)

welcome_msg = """
Добро пожаловать в Персональный помощник!
Выберите действие:
1. Управление заметками
2. Управление задачами
3. Управление контактами
4. Управление финансовыми записями
5. Калькулятор
6. Выход
"""


def exit_program():
    print("До свидания!")


def handle_choice_main():

    while True:
        print(welcome_msg)
        choice = input("Выберите действие: ")

        if choice == "1":
            note_controller.handle_choice()
        elif choice == "2":
            task_controller.handle_choice()
        elif choice == "3":
            contact_controller.handle_choice()
        elif choice == "4":
            finance_controller.handle_choice()
        elif choice == "5":
            pass
        elif choice == "6":
            exit_program()
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие от 1 до 6.")
            handle_choice_main()


handle_choice_main()
