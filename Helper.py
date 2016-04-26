import json
import unittest

from Book import Book


def create_books_list(books_decoded):
    books_list = []

    for book_dict in books_decoded:
        books_list.append(Book(**book_dict))

    return books_list


def get_books_cost_less_equals(books, cost):
    return filter(lambda book: book.cost <= cost, books)


def get_books_json():
    with open("books.json") as f:
        return f.read()


def get_books_list():
    books_json = get_books_json()
    books_json_decoded = json.loads(books_json)  # raw python objects: list of dicts

    return create_books_list(books_json_decoded)


class TestHelper(unittest.TestCase):
    def test_get_books_less_equals(self):
        suitable_books = \
            [Book(title="title 1", cost=100), Book(title="title 2", cost=200), Book(title="title 3", cost=300)]
        books = suitable_books + [Book(title="title 4", cost=400)]

        cost_to_check = 300

        self.assertListEqual(list(get_books_cost_less_equals(books, cost_to_check)), suitable_books)


if __name__ == "__main__":
    unittest.main()
