
from .FileHandler import FileHandler
from .Item import Item
from flask import Flask 
from flask import flash
from flask import send_file
from flask import render_template, redirect, url_for
from flask import request, make_response
from flask import session


import re
import os
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDjRLpE5kpL82vkQbJB9wRJC6mP1iR6o7w",
    "authDomain": "invoices-d12ae.firebaseapp.com",
    "databaseURL": "https://invoices-d12ae.firebaseio.com",
    "projectId": "invoices-d12ae",
    "storageBucket": "invoices-d12ae.appspot.com",
    "messagingSenderId": "741972661830",
    "appId": "1:741972661830:web:2a8ecdb51a559ce5881c47",
    "measurementId": "G-7BKRLPKX63"
}

# global variables
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


data = None
itemsList = []
foundData = [] # this is data found that is searched
fileName = ""
clientName = None

app = Flask(__name__)
app.secret_key = "namanjain"

def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) 




@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/home", methods=['GET', 'POST'])
def home():
    global clientName
    global itemsList
    global foundData
    isClientSelected = False

    if(clientName != None ):
        isClientSelected = True

    if request.method == 'POST':
        if (request.form['submit'] == 'add'):
            #mandatory
            # TODO: check with db to make sure name does not exist already 
            name = request.form["nm"]
            searchDB = searchItems(name, isExact = True)
            if(searchDB): # we found a copy
                flash("Item already exists in the database")
            else:
                costPrice = (request.form["cp"])
                salesPrice = (request.form["sp"])
                quantity = (request.form["quantity"])

                if name != '' and costPrice != '' and salesPrice != '' and quantity != '':
                    costPrice = float(costPrice)
                    salesPrice = float(salesPrice)
                    quantity = float(quantity)
                
                    #optional 
                    notes = None
                    notes = request.form["notes"]

                    if quantity > 0 and salesPrice > 0: # create item in db
                        
                        key = db.child("Products").push(
                            {"name": name,
                            "costPrice": costPrice, 
                            "previousSalePrice": [0,salesPrice],
                            "notes": notes,
                            "quantity": quantity
                            }
                        )
                        
                        jsonVal = Item(key, name, costPrice, salesPrice, notes, quantity)
                        itemsList.append(jsonVal)
                    else:
                        flash("Quantity and sales price must be larger than 0")
                else:
                    flash("Invaild Item")

            return render_template('main.html', data = data , 
            itemsList = itemsList, 
            isClientSelected = isClientSelected, 
            clientName = clientName )
            # return redirect( url_for("itemPage") )

        elif (request.form['submit'] == 'find'):
            findnm = request.form["findnm"]
            foundData = searchItems(findnm)
            return render_template('main.html', data = data, foundData = foundData, itemsList = itemsList, isClientSelected = isClientSelected,  clientName = clientName  )

        elif (request.form['submit'] == 'add_update'):
            #get form data
            itemUpdateKey = request.form["itemUpdateKey"]
            newName = request.form["newName"]
            newCostPrice = (request.form["newCostPrice"])
            addNewSalesPrice = (request.form["addNewSalesPrice"])
            newQuantity = (request.form["newQuantity"])
            if( not(itemUpdateKey and newName and newCostPrice and addNewSalesPrice and newQuantity)):
                flash("There are some missing parameters")
            else:
                newCostPrice = float(newCostPrice)
                addNewSalesPrice = float(addNewSalesPrice)
                newQuantity = float(newQuantity)

                thisItem = None
                hasChanged = False

                #check for changes that are vaild and update Item
                for item in foundData:
                    if item.key == itemUpdateKey:
                        thisItem = item
                        break

                if thisItem:
                    if( newName == ''):
                        flash("name must not be empty")
                    elif(newCostPrice <= 0 or addNewSalesPrice <=0 or newQuantity <= 0 ):
                        flash("all values must be non null and must be greater than 0 ")
                    else:
                        if newName and newName != thisItem.name :
                            thisItem.name = newName
                            print("Changed because of name : ")
                            hasChanged = True
                        if newCostPrice and newCostPrice != thisItem.costPrice:
                            thisItem.costPrice = newCostPrice
                            hasChanged = True
                            print("Changed because of costprice : ")
                        if addNewSalesPrice and addNewSalesPrice != thisItem.previousSalePrice[-1]:
                            thisItem.previousSalePrice.append(addNewSalesPrice) 
                            hasChanged = True
                            print("Changed because of salesprice : ")
                        if newQuantity and newQuantity != thisItem.quantity:
                            #TODO: Throw error if new Quantity is 0 
                            thisItem.quantity = newQuantity
                            hasChanged = True
                            print("Changed because of quantity : ")

                        itemsList.append(thisItem) # add this to the list of items in the invoice
                        if(hasChanged):
                            #update db values
                            db.child("Products").child(itemUpdateKey).update(thisItem.createDBString())
            return render_template('main.html', data = data, itemsList = itemsList, isClientSelected = isClientSelected,  clientName = clientName  )
                

        elif (request.form['submit'] == 'remove'):
            toDelete  = request.form["itemDelete"]
            for item in itemsList:
                if (item.name == toDelete):
                    itemsList.remove(item)
                break
                    
            return render_template('main.html', data = data, itemsList = itemsList, isClientSelected = isClientSelected,  clientName = clientName  )
        
        elif(request.form['submit'] == 'updateClientName'):
            itemsList = []
            check = request.form["cname"]
            if(isValidFileName(check)):
                clientName = request.form["cname"]
                isClientSelected = True
            else:
                flash('Invalid Filename: ' + check)
            return render_template('main.html', data = data, itemsList = itemsList, isClientSelected = isClientSelected,  clientName = clientName )

        else:
            return render_template('main.html', data = data, itemsList = itemsList, isClientSelected = isClientSelected,  clientName = clientName  )
    else:
        return render_template('main.html', data = data, itemsList = itemsList, isClientSelected = isClientSelected,  clientName = clientName   )

@app.route("/logout")
def logout():
    session.pop("home", None)
    return redirect(url_for("login"))

def findByKeyWord(word):
    itemsByName = db.child("Products").order_by_child('name').get()
    print(itemsByName)
    return f"<h1>{itemsByName}</h1>"


@app.route('/return-files')
def creareturn_files_tut():
    global itemsList
    global clientName
    try:
        if len(itemsList) <= 0:
            flash("The itemList was found to contain no items")
        else:
            taxPercent = 0.13
            ziped = FileHandler(clientName, itemsList, taxPercent)
            file = ziped.addToZip()
            os.remove(ziped.excelFileName)
            os.remove(ziped.wordFileName)
            # os.remove(file)
            itemsList = []
            clientName = None
            response = make_response(send_file(file, file, as_attachment=True))

            # remove cache for the file so that a new file can be sent each time
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            response.headers['Cache-Control'] = 'public, max-age=0'

            return response
        # return out
    except Exception as e:
        return str(e)

@app.route('/change-client')
def resetClientName():
    global clientName

    #reset clientName
    clientName = None
    return redirect(url_for('home'))
    

def isValidFileName(name):
    if all(x.isalpha() or x.isspace() or x.isnumeric() for x in name):
        return True
    else:
        return False

def getData():
    global data
    data = None
    data = db.child("Products").get()
    # print(data)

def searchItems(query, isExact = False):
    getData()
    # parsing = re.search('te', "TEST", re.IGNORECASE)
    
    listToShare = [] # this list contains all found products and their details
    temp_name = None
    temp_costPrice = None
    temp_salesPrice = None
    temp_quantity = None
    isAll = False

    if(query == None or query == ""):
        return None
    if(query == "*"): # master key to see all items in db
        isAll = True
    if(isExact):
        for i in data.each():
            if(i.val()["name"] == query ):
                return True # this is used for adding a new item to the database. The if the new item we are adding exists in the db we will not add it.
        return False;
    for i in data.each():
        try:
            temp_name = i.val()["name"]
            check = re.search( query, temp_name, re.IGNORECASE )
            if(check or (isAll and temp_name)): # it was found that this is a match to our query
                temp_costPrice = (i.val()["costPrice"])

                temp_salesPrice = (i.val()["previousSalePrice"])
                temp_quantity = i.val()["quantity"]
                notes = "Previous Sales Prices Were: " + str(i.val()["previousSalePrice"])
                if i.val()["notes"]:
                    notes = notes + " / " + i.val()["notes"]

                key = i.key()
                jsonVal = Item(key, temp_name, temp_costPrice, temp_salesPrice, i.val()["notes"], temp_quantity) # include the old note to prevent the temp note from overwriting
                listToShare.append(jsonVal)
                jsonVal.printItem()
        except:
            print("Found object dictionary has missing params") 
        
    return listToShare


    

