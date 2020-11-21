import http.server
import socketserver
import io
import xlsxwriter
import datetime

class Item:
    def __init__(self, key, name, costPrice, previousSalePrice , notes, quantity):
        self.key = key
        self.name = name
        self.costPrice = costPrice
        self.previousSalePrice = previousSalePrice
        self.notes = notes
        self.quantity = quantity

class ExcelMaker:
    def __init__(self, title, items, taxPercent):
        self.filename  = title
        self.items = items
        self.taxPercent = taxPercent
        self.total = 0
        self.subTotal = 0
        self.hst = 0

        self.calTotal()

    def calTotal(self):
        self.subTotal = 0 
        for item in self.items:
            self.subTotal += item.quantity * item.previousSalePrice
        self.hst =  self.subTotal * self.taxPercent
        self.total = self.subTotal + self.hst
        print(self.total)

    def makeExcel(self):
        if self.items:
            workbook = xlsxwriter.Workbook(self.filename + ".xlsx")
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, "Product Name")
            worksheet.write(0, 1, "Price")
            worksheet.write(0, 2, "Quantity")
            worksheet.write(0, 3, "Total")
            i = 1
            for item in self.items:
                print("PRINTING", item)
                worksheet.write(i + 1, 0, item.name )
                worksheet.write(i + 1, 1, item.previousSalePrice )
                worksheet.write(i + 1, 2, item.quantity )
                worksheet.write(i + 1, 3, item.quantity * item.previousSalePrice  )
                i += 1   
            
            worksheet.write(i + 1, 0, "Sub Total" )
            worksheet.write(i + 2, 0, "HST" )
            worksheet.write(i + 3, 0, "Total" )

            worksheet.write(i + 1, 3, self.subTotal )
            worksheet.write(i + 2, 3, self.hst )
            worksheet.write(i + 3, 3, self.total )
            workbook.close()
            return self.filename + ".xlsx" # save file to machine
        else:
            return None

    # def get_xslx_for_data(self, filename, title):
        # try:
        #     output = io.BytesIO()
        #     workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        #     worksheet = workbook.add_worksheet(filename)
        #     worksheet.write(0, 0, title)
        #     worksheet.write(1, 0, "Product Name")
        #     worksheet.write(1, 1, "Price")
        #     worksheet.write(1, 2, "Quantity")
        #     worksheet.write(1, 3, "Total")
        #     i = 2
        #     for item in self.items:
        #         worksheet.write(i + 1, 0, item.name )
        #         worksheet.write(i + 1, 1, item.previousSalePrice )
        #         worksheet.write(i + 1, 2, item.quantity )
        #         worksheet.write(i + 1, 3, item.quantity * item.previousSalePrice  )
        #         i += 1   
            
        #     worksheet.write(i + 1, 0, "Sub Total" )
        #     worksheet.write(i + 2, 0, "HST" )
        #     worksheet.write(i + 3, 0, "Total" )

        #     worksheet.write(i + 1, 3, self.subTotal )
        #     worksheet.write(i + 2, 3, self.hst )
        #     worksheet.write(i + 3, 3, self.total )
        #     workbook.close()

        #      # Rewind the buffer.
        #     output.seek(0)

        #     response.data = filename + ".xlsx"
        #     file_name = 'my_file_{}.xlsx'.format(
        #         datetime.now().strftime('%d/%m/%Y'))
        #     mimetype_tuple = mimetypes.guess_type(file_name)
        #     response_headers = Headers({
        #         'Pragma': "public",  # required,
        #         'Expires': '0',
        #         'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
        #         'Cache-Control': 'private',  # required for certain browsers,
        #         'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        #         'Content-Disposition': 'attachment; filename=\"%s\";' % file_name,
        #         'Content-Transfer-Encoding': 'binary',
        #         'Content-Length': len(response.data)
        #     })

        #     if not mimetype_tuple[1] is None:
        #         response.update({
        #             'Content-Encoding': mimetype_tuple[1]
        #         })
        #     response.headers = response_headers
        #     response.set_cookie('fileDownload', 'true', path='/')
        #     return response
        # except Exception as e:
        #     print(e)

