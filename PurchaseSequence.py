class PurchaseSequence:
    purchases = []

    def __init__(self, purchases):
        self.purchases = purchases

    def add_purchase(self, purchase):
        if not purchase.is_empty_purchase():
            self.purchases.append(purchase)
        return self

    def add_purchases(self, purchases):
        self.purchases.append(purchases)

        return self

    def get_total_cost(self):  # TODO calculation caching
        costs = map(lambda purchase: purchase.get_cost(), self.purchases)
        return sum(costs)

    def __repr__(self):  # TODO not correct
        return "\n\nPurchaseSequence({}, total_cost:{})".format(str(self.purchases), self.get_total_cost())

    def __str__(self):
        return self.__repr__()
