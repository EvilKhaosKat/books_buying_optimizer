import json
import unittest
import itertools

from Book import Book
from Purchase import Purchase
from PurchaseSequence import PurchaseSequence

BOUGHT_BOOKS_IN_ONE_PURCHASE = 3


def create_books_list(books_decoded):
    books_list = []

    for book_dict in books_decoded:
        books_list.append(Book(**book_dict))

    return books_list


def get_books_cost_less_equals(books, cost):
    return filter(lambda book: book.cost <= cost, books)


def _get_books_json():
    with open("books.json") as f:
        return f.read()


def get_books_list():
    books_json = _get_books_json()
    books_json_decoded = json.loads(books_json)  # raw python objects: list of dicts

    return create_books_list(books_json_decoded)


def add_in_top_if_suits(purchase_sequences_top, current_purchase_sequence):
    print("purchase_sequences_top:%s" % purchase_sequences_top)
    print("current_purchase_sequence:%s" % current_purchase_sequence)

    current_cost = current_purchase_sequence.get_total_cost()

    top_costs = map(lambda purchase_sequence: purchase_sequence.get_total_cost(), purchase_sequences_top)
    max_top_cost = _get_max_top_cost(top_costs)

    print("current_cost:%s" % current_cost)
    print("max_top_cost:%s" % max_top_cost)

    if current_cost < max_top_cost:
        purchase_sequences_top.append(current_purchase_sequence)


def _get_max_top_cost(top_costs):
    if len(top_costs) == 0:
        return 0
    else:
        return max(top_costs)


def get_purchase_variants(books_list, best_variants_count, current_purchase_sequence=None, purchase_sequences_top=None):
    books_list = books_list[:]  # copy

    if not purchase_sequences_top:
        purchase_sequences_top = []
    if not current_purchase_sequence:
        current_purchase_sequence = PurchaseSequence()

    if len(books_list) <= BOUGHT_BOOKS_IN_ONE_PURCHASE:  # leftovers - by as is all of them
        current_purchase_sequence.add_purchase(Purchase(bought_books=books_list[:]))
        add_in_top_if_suits(purchase_sequences_top, current_purchase_sequence)
    else:
        books_combinations = itertools.combinations(books_list, BOUGHT_BOOKS_IN_ONE_PURCHASE)
        for books_combination in books_combinations:  # check all books groups to buy combinations
            purchase = Purchase(bought_books=books_combination)
            min_cost = purchase.get_minimum_cost()

            leftovers_books = _substract_lists(books_list, books_combination)
            free_getting_books = get_books_cost_less_equals(leftovers_books, min_cost)

            for free_book in free_getting_books:  # check all free books possible variants
                purchase.free_book = free_book

                other_books = leftovers_books[:]
                other_books.remove(free_book)

                current_purchase_sequence.add_purchase(purchase)

                get_purchase_variants(books_list=other_books,
                                      best_variants_count=best_variants_count,
                                      current_purchase_sequence=current_purchase_sequence,
                                      purchase_sequences_top=purchase_sequences_top)

    return purchase_sequences_top


def _substract_lists(books_list, books_combination):
    return list(set(books_list) - set(books_combination))


class TestHelper(unittest.TestCase):
    def test_get_books_less_equals(self):
        suitable_books = \
            [Book(title="title 1", cost=100), Book(title="title 2", cost=200), Book(title="title 3", cost=300)]
        books = suitable_books + [Book(title="title 4", cost=400)]

        cost_to_check = 300

        self.assertListEqual(list(get_books_cost_less_equals(books, cost_to_check)), suitable_books)


if __name__ == "__main__":
    unittest.main()