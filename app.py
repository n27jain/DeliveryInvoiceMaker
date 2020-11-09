from flask import Flask 
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request


app = Flask(__name__)

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
        postItem = request.form["productEntry"]
        print("postItem is" ,  postItem)
        return redirect( url_for("itemPage", item = postItem) )
    else:
        return render_template('main.html')

@app.route("/itemPage") 
def itemPage(item):
    return f"<h1> item </h1>"







if __name__ == '__main__':
    app.run(debug=True)


