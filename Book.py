class Book:
    title = "No title"
    cost = 0

    def __init__(self, title, cost):
        self.title = title
        self.cost = cost

    def __eq__(self, other):
        return self.__dict__ == other.__dict__  # TODO check strictly on title/cost?

    def __repr__(self):
        return "Book(title='{}', cost={})".format(self.title, self.cost)

    def __str__(self, *args, **kwargs):
        return self.__repr__()

    def __hash__(self):
        return hash(self.title) ^ hash(self.cost)
