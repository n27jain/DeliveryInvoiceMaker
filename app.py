import pyrebase
from flask import Flask 
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session
from flask import config



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

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
app = Flask(__name__)
app.secret_key = "namanjain"
data = None
itemsList = []
class Item:
    def __init__(self, key, name, costPrice, previousSalePrice , notes, quantity):
        self.key = key
        self.name = name
        self.costPrice = costPrice
        self.previousSalePrice = previousSalePrice
        self.notes = notes
        self.quantity = quantity



def getData():
    data = None
    data = db.child("Products").get()
    return data

# Route for handling the login page logic
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

    found = [] # this will be the list of found items in the database
    search = None # this will be the keyword we search by

    data = getData()
    global itemsList

    if request.method == 'POST':
        if (request.form['submit'] == 'add'):

            #mandatory
            item = request.form["nm"]
            costPrice = request.form["cp"]
            salesPrice = request.form["sp"]
            quantity = request.form["quantity"]
            #optional 
            notes = None
            notes = request.form["notes"]

            if item and costPrice and salesPrice and quantity: # create item in db
                varcheck = db.child("Products").push(
                    {"name": item,
                    "costPrice": costPrice, 
                    "previousSalePrice": [0,salesPrice],
                    "notes": notes,
                    "quantity": quantity
                    }
                )
              
                data = getData()
                jsonVal = Item(varcheck, item, costPrice, salesPrice, notes, quantity)
                itemsList.append(jsonVal)
                print("LENGTH:" ,len(itemsList))

            session["item"] = item
            print("postItem is" ,  item)
            return render_template('main.html', data = data , itemsList = itemsList )
            # return redirect( url_for("itemPage") )

        elif (request.form['submit'] == 'find'):
            findnm = request.form["findnm"]
            print("findnm is" , findnm)
            # return findByKeyWord(findnm)
            #return render_template('main.html', data = None )

        elif (request.form['submit'] == 'remove'):
            toDelete  = request.form["itemDelete"]
            al = db.child("Products").child(toDelete).get()
            al = al.val()
            print("itemNameToDelete: ", toDelete)
            print("finding :", al)
            db.child("Products").child(toDelete).remove()
            data = getData()
            return render_template('main.html', data = data, itemsList = itemsList)

        else:
            return render_template('main.html', data = data, itemsList = itemsList )

    else:
            return render_template('main.html', data = data, itemsList = itemsList )

@app.route("/logout")
def logout():
    session.pop("home", None)
    return redirect(url_for("login"))



def findByKeyWord(word):
    itemsByName = db.child("Products").order_by_child('name').get()
    print(itemsByName)
    return f"<h1>{itemsByName}</h1>"



if __name__ == '__main__':
    app.run(debug=True)


