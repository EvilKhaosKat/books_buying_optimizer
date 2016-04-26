import json


def get_books_json():
    with open("books.json") as f:
        return f.read()


books_json = get_books_json()
print("books_json:%s" % books_json)


books_decoded = json.loads(books_json)
