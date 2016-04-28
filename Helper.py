import json
import unittest
import itertools
import sys
import copy

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
    purchase_sequence_obj = PurchaseSequence(current_purchase_sequence)
    # purchase_sequence_obj.purchases = current_purchase_sequence

    current_cost = purchase_sequence_obj.get_total_cost()

    top_costs = list(map(lambda purchase_sequence: purchase_sequence.get_total_cost(), purchase_sequences_top))
    max_top_cost = _get_max_top_cost(top_costs)

    if current_cost < max_top_cost:
        purchase_sequences_top.append(purchase_sequence_obj)


def _get_max_top_cost(top_costs):
    if len(top_costs) == 0:
        return sys.maxsize
    else:
        return max(top_costs)


def _get_books_from_purchases_list(current_purchase_sequence):
    books = []

    for purchase in current_purchase_sequence:
        bought_books = purchase.bought_books
        if bought_books:
            books.extend(bought_books)

        free_book = purchase.free_book
        if free_book:
            books.append(free_book)

    return books


def get_purchase_variants(books_list, best_variants_count):
    variants = _get_purchase_variants(books_list=books_list)

    variants = sorted(variants, key=lambda purchase_sequence: purchase_sequence.get_total_cost(), reverse=False)
    variants = variants[:best_variants_count]

    return variants


def _get_purchase_variants(books_list, current_purchase_sequence=None, purchase_sequences_top=None):
    books_list = books_list[:]  # copy

    if not purchase_sequences_top:
        purchase_sequences_top = []

    if not current_purchase_sequence:
        current_purchase_sequence = []

    if len(books_list) <= BOUGHT_BOOKS_IN_ONE_PURCHASE:  # leftovers - buy all of them as is
        # print("add leftovers:%s" % books_list)
        current_purchase_sequence = current_purchase_sequence[:]
        current_purchase_sequence.append(Purchase(bought_books=books_list[:]))

        # add_in_top_if_suits(purchase_sequences_top, current_purchase_sequence)
        purchase_sequences_top.append(PurchaseSequence(current_purchase_sequence))
    else:
        books_combinations = itertools.combinations(books_list, BOUGHT_BOOKS_IN_ONE_PURCHASE)
        for books_combination in books_combinations:  # check all books groups to buy combinations
            purchase = Purchase(bought_books=books_combination)
            min_cost = purchase.get_minimum_cost()

            leftovers_books = _substract_lists(books_list, books_combination)
            #from_purchases_list = _get_books_from_purchases_list(current_purchase_sequence)
            #leftovers_books = _substract_lists(leftovers_books,
            #                                   from_purchases_list)  # TODO for some reasons not all the used books removed - causes problems

            free_getting_books = list(get_books_cost_less_equals(leftovers_books, min_cost))

            for free_book in free_getting_books:  # check all free books possible variants
                purchase.free_book = free_book

                other_books = leftovers_books[:]
                other_books.remove(free_book)

                modified_purchase_sequence = current_purchase_sequence[:]
                modified_purchase_sequence.append(purchase)  # TODO problem is here

                purchase_sequences_top = _get_purchase_variants(books_list=other_books,
                                                                current_purchase_sequence=modified_purchase_sequence[:],
                                                                purchase_sequences_top=purchase_sequences_top)

    return purchase_sequences_top


def _substract_lists(books_list, books_combination):
    result_books_list = books_list[:]

    for book_to_remove in books_combination:
        if book_to_remove in result_books_list:
            result_books_list.remove(book_to_remove)

    return result_books_list
    # return list(set(books_list) - set(books_combination))


class TestHelper(unittest.TestCase):
    def test_substract_lists(self):
        list_1 = [Book(title="Title 1", cost=100), Book(title="Title 2", cost=100), Book(title="Title 3", cost=100)]
        list_2 = [Book(title="Title 2", cost=100), Book(title="Title 3", cost=100), Book(title="Title 4", cost=100)]

        self.assertListEqual(_substract_lists(list_1, list_2), [Book(title="Title 1", cost=100)])

    def test_get_books_less_equals(self):
        suitable_books = \
            [Book(title="title 1", cost=100), Book(title="title 2", cost=200), Book(title="title 3", cost=300)]
        books = suitable_books + [Book(title="title 4", cost=400)]

        cost_to_check = 300

        self.assertListEqual(list(get_books_cost_less_equals(books, cost_to_check)), suitable_books)


if __name__ == "__main__":
    unittest.main()
