from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

#setting up the app
app = Flask(__name__)
#secret key to use session
app.secret_key = "secretkey"

#setting up db

#creating the tables

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("recipes.html", title = "CS50 Bakery")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method != 'POST':
        return render_template('register.html')
    else:
        user =  request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password-confirmation"]
        
        if user == "" or password == "" or password_confirm == "":
            flash('Please fill all the fields to proceed.', 'info')
            return render_template("register.html", user = user)
        
        elif password != password_confirm:
            flash('Password did not match.', 'info')
            return render_template("register.html", user = user)
        
        
        session["user_id"] = user
        return redirect('/')

    
@app.route("/login", methods=["GET", "POST"])
def login():
    return redirect('/')

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run()

