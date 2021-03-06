from datetime import datetime
from zipfile import ZipFile
from .ExcelMaker import ExcelMaker
from .WordMaker import WordMaker

class FileHandler:
    def __init__(self, clientName, itemsList, taxPercent, header):
        self.clientName = clientName
        self.itemsList = itemsList
        self.taxPercent = taxPercent

        self.header = header
        self.time = datetime.today()
        self.dateString = ""+ str(self.time.month) + "/"+ str(self.time.day) + "/" + str( self.time.year)

        self.clientFileName = self.clientName + str(self.time)
        self.personalFile = "PERSONAL_" + self.clientName + str(self.time)

        self.excelFileName = self.makeExcel()
        self.wordFileName = self.makeWord()
    
    def makeExcel(self):
        mkr = ExcelMaker(clientName = self.clientName, fileName= self.clientFileName, items = self.itemsList, taxPercent= self.taxPercent)
        print("Here:  " , self.clientFileName )
        return mkr.makeExcel()
    
    def makeWord(self):
        wordFile = WordMaker(clientName = self.clientName, 
        fileName = self.clientFileName, 
        itemList = self.itemsList, 
        taxPercent = self.taxPercent,
        header = self.header)
        return wordFile.save()

    def addToZip(self):
        zip = ZipFile("app/"+ self.clientFileName + ".zip", 'w')
        zip.write(self.excelFileName);
        zip.write(self.wordFileName)
        zip.close()
        return ( self.clientFileName + ".zip")