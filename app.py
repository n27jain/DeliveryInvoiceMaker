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

db.child("Products").push({"name": "Thermometer", "costPrice": "10.50", "previousSalePrice": [15,20,15,16]})

app = Flask(__name__)
app.secret_key = "namanjain"
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
    if request.method == 'POST':
        item = request.form["nm"]
        session["item"] = item
        print("postItem is" ,  item)
        return redirect( url_for("itemPage") )
    else:
        return render_template('main.html')

@app.route("/item")
def itemPage():
    if "item" in session:
        item = session["item"]
        return f"<h1>{item}</h1>"
    else:
        redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop("home", None)
    return redirect(url_for("login"))



if __name__ == '__main__':
    app.run(debug=True)


