class Purchase:
    bought_books = []
    free_book = None

    def __init__(self, bought_books, free_book):
        self.bought_books = bought_books
        self.free_book = free_book

    def __repr__(self):
        return "Purchase(bought_books={}, free_book={}".format(self.bought_books, self.free_book)

    def __str__(self):
        return self.__repr__()



