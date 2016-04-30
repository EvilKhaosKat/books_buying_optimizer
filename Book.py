import unittest


class Book:
    title = "No title"
    cost = 0

    def __init__(self, title, cost):
        self.title = title
        self.cost = cost

    def __eq__(self, other):
        return self.title == other.title  # TODO check strictly on title/cost?

    def __repr__(self):
        return "Book(title='{}', cost={})".format(self.title, self.cost)

    def __str__(self, *args, **kwargs):
        return self.__repr__()

    def __hash__(self):
        return hash(self.title) ^ hash(self.cost)


class TestBook(unittest.TestCase):
    def test_equals(self):
        book_1 = Book(title='Book 1', cost=1)
        book_1_copy = Book(title='Book 1', cost=1)

        book_2 = Book(title='Book 2', cost=2)

        self.assertEqual(book_1, book_1_copy)
        self.assertNotEqual(book_1, book_2)
