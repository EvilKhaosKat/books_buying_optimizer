import json

from Book import Book


def get_books_json():
    with open("books.json") as f:
        return f.read()


def create_books_list(books_decoded):
    books_list = []

    for book_dict in books_decoded:
        books_list.append(Book(**book_dict))

    return books_list


books_json = get_books_json()


print("books_json:%s" % books_json)


books_json_decoded = json.loads(books_json)  # raw python objects: list of dicts
books_list = create_books_list(books_json_decoded)

print("books_list:%s" % books_list)
