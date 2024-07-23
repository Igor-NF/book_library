import json
import os


class Book:
    def __init__(self, book_id, title, author, year, status='в наличии'):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status,
        }

    @staticmethod
    def from_dict(data):
        return Book(data['id'], data['title'], data['author'], data['year'], data['status'])


class Library:
    def __init__(self, filename='library.json'):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        return []

    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        book_id = self.generate_id()
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f'Книга "{title}" ({author} {year}г.) добавлена с ID {book_id}.')

    def generate_id(self):
        return max([book.id for book in self.books], default=0) + 1

    def delete_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f'Книга с ID {book_id} удалена.')
                return
        print(f'Ошибка: Книга с ID {book_id} не найдена.')

    def search_books(self, search_term):
        found_books = [book for book in self.books if (
                search_term.lower() in book.title.lower() or
                search_term.lower() in book.author.lower() or
                search_term == str(book.year))]

        if found_books:
            print("Найдены книги:")
            for book in found_books:
                print(
                    f'ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}')
        else:
            print('Книги не найдены.')

    def display_books(self):
        if not self.books:
            print('Библиотека пуста.')
            return

        print("Список всех книг:")
        for book in self.books:
            print(
                f'ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}')

    def change_status(self, book_id, new_status):
        for book in self.books:
            if book.id == book_id:
                if new_status in ['в наличии', 'выдана']:
                    book.status = new_status
                    self.save_books()
                    print(f'Статус книги с ID {book_id} изменен на "{new_status}".')
                else:
                    print('Ошибка: Неверный статус. Используйте "в наличии" или "выдана".')
                return
        print(f'Ошибка: Книга с ID {book_id} не найдена.')


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")

        choice = input("Выберите номер команды из списка меню: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)
        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.delete_book(book_id)
        elif choice == '3':
            search_term = input("Введите название, автора или год для поиска: ")
            library.search_books(search_term)
        elif choice == '4':
            library.display_books()
        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус (в наличии/выдана): ")
            library.change_status(book_id, new_status)
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
