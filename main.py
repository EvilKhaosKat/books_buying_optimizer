import itertools

from Helper import _get_books_list

BOUGHT_BOOKS_IN_ONE_PURCHASE = 3

books_list = _get_books_list()

print("books_list:%s" % books_list)


bought_books_combinations = itertools.combinations(books_list, BOUGHT_BOOKS_IN_ONE_PURCHASE)
print("bought_books_combinations:%s" % list(bought_books_combinations))
