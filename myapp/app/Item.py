class Item:
    def __init__(self, key, name, costPrice, previousSalePrice , notes, quantity):
        self.key = key
        self.name = name
        self.costPrice = costPrice
        self.previousSalePrice = previousSalePrice
        self.notes = notes
        self.quantity = quantity
    def printItem(self):
        print(
            "key  :", self.key,
            "name  :",self.name,
            "costPrice  :",self.costPrice,
            "previousSalePricevious  :",self.previousSalePrice,
            "notes  :",self.notes,
            "quantity  :",self.quantity
        )