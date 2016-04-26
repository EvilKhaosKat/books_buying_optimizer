import unittest

from Book import Book


class Purchase:
    bought_books = []
    free_book = None

    def __init__(self, bought_books, free_book=None):
        self.bought_books = bought_books
        self.free_book = free_book

    def __repr__(self):
        return "Purchase(bought_books={}, free_book={}".format(self.bought_books, self.free_book)

    def __str__(self):
        return self.__repr__()

    def get_cost(self):
        """
        Returns cost sum of bought books
        """

        bought_books_costs = self._get_books_costs()
        return sum(bought_books_costs)

    def _get_books_costs(self):
        return list(map(lambda book: book.cost, self.bought_books))

    def get_minimum_cost(self):
        return min(self._get_books_costs())


class TestPurchase(unittest.TestCase):
    def _get_stub_books(self):
        return [Book(title="title 1", cost=100), Book(title="title 2", cost=200), Book(title="title 3", cost=300)]

    def test_get_cost(self):
        bought_books = self._get_stub_books()
        free_book = Book(title="Free book", cost=10)

        purchase = Purchase(bought_books=bought_books, free_book=free_book)
        self.assertEqual(purchase.get_cost(), 600)

    def test_min_cost(self):
        bought_books = self._get_stub_books()
        purchase = Purchase(bought_books=bought_books)

        self.assertEqual(purchase.get_minimum_cost(), 100)


if __name__ == "__main__":
    unittest.main()
