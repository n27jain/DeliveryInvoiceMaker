import xlsxwriter
from .Item import Item


class ExcelMaker:
    def __init__(self, clientName, fileName, items, taxPercent):
        self.clientname  = clientName
        self.fileName = fileName
        self.items = items
        self.taxPercent = taxPercent
        self.total = 0
        self.subTotal = 0
        self.hst = 0

        self.calTotal()

    def calTotal(self):
        self.subTotal = 0 
        for item in self.items:
            self.subTotal += item.quantity * item.previousSalePrice[-1]
        self.hst =  self.subTotal * self.taxPercent
        self.total = self.subTotal + self.hst
        # print(self.total)

    def makeExcel(self):
        if self.items:
            print("here again : ", self.fileName)
            workbook = xlsxwriter.Workbook("app/"+self.fileName + ".xlsx")
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, "Product Name")
            worksheet.write(0, 1, "Price")
            worksheet.write(0, 2, "Quantity")
            worksheet.write(0, 3, "Total")
            i = 1
            for item in self.items:
                worksheet.write(i + 1, 0, item.name )
                worksheet.write(i + 1, 1, item.previousSalePrice[-1] )
                worksheet.write(i + 1, 2, item.quantity )
                worksheet.write(i + 1, 3, item.quantity * item.previousSalePrice[-1]  )
                i += 1   
            
            worksheet.write(i + 1, 0, "Sub Total" )
            worksheet.write(i + 2, 0, "HST" )
            worksheet.write(i + 3, 0, "Total" )

            worksheet.write(i + 1, 3, self.subTotal )
            worksheet.write(i + 2, 3, self.hst )
            worksheet.write(i + 3, 3, self.total )
            workbook.close()
            return "app/"+ self.fileName + ".xlsx" # save file to machine
        else:
            return None

