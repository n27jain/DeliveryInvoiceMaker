class Item:
    def __init__(self, key, name, costPrice, previousSalePrice , notes, quantity):
        self.key = key
        self.name = name
        self.costPrice = costPrice
        self.previousSalePrice = previousSalePrice
        self.notes = notes
        self.quantity = quantity
    def printItem(self):
        print( "printing Item details : ",
            "key  :", self.key,
            "name  :",self.name,
            "costPrice  :",self.costPrice,
            "previousSalePrices  :",self.previousSalePrice,
            "notes  :",self.notes,
            "quantity  :",self.quantity
        )
    def createDBString(self):
        return {"name": self.name,
                    "costPrice": self.costPrice, 
                    "previousSalePrice": self.previousSalePrice,
                    "notes": self.notes,
                    "quantity": self.quantity
                    }
