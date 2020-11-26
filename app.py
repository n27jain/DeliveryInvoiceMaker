
from FileHandler import FileHandler
from Item import Item

from flask import Flask 
from flask import flash
from flask import send_file
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session

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
fileName = ""
clientName = None

app = Flask(__name__)
app.secret_key = "namanjain"






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
    data = getData()
    isClientSelected = False

    if(clientName != None ):
        isClientSelected = True

    if request.method == 'POST':
        if (request.form['submit'] == 'add'):
            #mandatory
            # TODO: check with db to make sure name does not exist already 
            name = request.form["nm"]
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
                    #TODO: Make sure to include this to add to the database
                    # key = db.child("Products").push(
                    #     {"name": name,
                    #     "costPrice": costPrice, 
                    #     "previousSalePrice": [0,salesPrice],
                    #     "notes": notes,
                    #     "quantity": quantity
                    #     }
                    # )

                    # key = key["name"]
                    key = 100
                    data = getData()
                    jsonVal = Item(key, name, costPrice, salesPrice, notes, quantity)
                    itemsList.append(jsonVal)
                else:
                    flash("Invaild Item")
            else:
                flash("Invaild Item")

            return render_template('main.html', data = data , 
            itemsList = itemsList, 
            isClientSelected = isClientSelected, 
            clientName = clientName )
            # return redirect( url_for("itemPage") )

        elif (request.form['submit'] == 'find'):
            findnm = request.form["findnm"]

        elif (request.form['submit'] == 'remove'):
            toDelete  = request.form["itemDelete"]
            for item in itemsList:
                if (item.name == toDelete):
                    itemsList.remove(item)
                    data = getData()
            return render_template('main.html', data = data, itemsList = itemsList, isClientSelected = isClientSelected,  clientName = clientName  )
        
        elif(request.form['submit'] == 'updateName'):
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
            return send_file(file, file,  as_attachment=True )
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
    data = None
    data = db.child("Products").get()
    return data



