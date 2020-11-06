import xlsxwriter

class ExcelMaker:
    def __init__(self, title, items, taxPercent):
        self.title  = title
        self.items = items
        self.taxPercent = taxPercent
        self.total = 0
        self.subTotal = 0
        self.hst = 0

        
    
    def calTotal(self):
        self.subTotal = 0 
        for i in range(len(self.items)):
            self.subTotal += self.items(i).quantity * self.items(i).price 
        self.hst =  self.subTotal * self.taxPercent
        self.total = self.subTotal + self.hst

    def makeExcel(self, filename, title):
        workbook = xlsxwriter.Workbook(filename + ".xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "title")
        worksheet.write(1, 0, "Product Name")
        worksheet.write(1, 1, "Price")
        worksheet.write(1, 2, "Quantity")
        worksheet.write(1, 3, "Total")
        i = 1
        # for i in range(len(self.items)):
        #     worksheet.write(i + 1, 0, self.items(i).name )
        #     worksheet.write(i + 1, 1, self.items(i).price )
        #     worksheet.write(i + 1, 2, self.items(i).quantity )
        #     worksheet.write(i + 1, 3, self.items(i).amount )
        
        worksheet.write(i + 1, 0, "Sub Total" )
        worksheet.write(i + 2, 0, "HST" )
        worksheet.write(i + 3, 0, "Total" )

        worksheet.write(i + 1, 3, self.subTotal )
        worksheet.write(i + 2, 3, self.hst )
        worksheet.write(i + 3, 3, self.total )


        workbook.close()
excelMaker = ExcelMaker ("File", 0, 0)   	

excelMaker.makeExcel("example", "File")



