from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

#setting up the app
app = Flask(__name__)
#secret key to use session
app.secret_key = "secretkey"

#setting up db -- table were created separately
conn = sqlite3.connect('bakery.db', check_same_thread=False)
c = conn.cursor()

#home page logic
@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" in session:
        return render_template("recipes.html", title = "Home", user_id = session["user_id"])
    else:
        return render_template("recipes.html", title = "Home")

#register logic
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method != 'POST':
        return render_template('register.html')
    else:
        username =  request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password-confirmation"]
        
        #check for empty inputs
        if username == "" or password == "" or password_confirm == "":
            flash('Please fill all the fields to proceed.', 'info')
            return render_template("register.html", username = username)
        
        #check for duplicates username
        elif c.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone() != None:
            flash('Username already taken, please try another.', 'info')
            return render_template("register.html", username = username)
        
        #check for password validity
        elif password != password_confirm:
            flash('Password did not match.', 'info')
            return render_template("register.html", username = username)

        #basic checks ok, create a hash for passwords and add the user
        password = generate_password_hash(password)
        data = (username, password)
        c.execute("INSERT INTO users (username, password) VALUES (?,?)", data)
        conn.commit()
        user_id = c.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        session["user_id"] = user_id[0]
        return redirect('/')

#login logic   
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method != 'POST':
        return render_template('login.html')
    else:
        #get form info
        username =  request.form["username"]
        password = request.form["password"]

        #check for empty inputs
        if username == "" or password == "":
            flash('Please fill all the fields to proceed.', 'info')
            return render_template("login.html", username = username)

        #check if username is in DB
        user_data = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user_data == None:
            flash('Unknown username, please register.', 'info')
            return render_template("register.html", username = username)

        #check password
        if check_password_hash(user_data[2], password) == False:
            flash('Password was incorrect, please try again.', 'info')
            return render_template("login.html", username = username)
        
        #login user, set session as user_id
        session["user_id"] = user_data[0]
        return redirect('/')

#logout logic to clear session
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')

#launch the app
if __name__ == "__main__":
    app.run()

