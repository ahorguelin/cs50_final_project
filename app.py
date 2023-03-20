from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

#setting up the app
app = Flask(__name__)
#secret key to use session
app.secret_key = "secretkey"
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

#setting up db -- table were created separately -- using row factory to get dictionaries
conn = sqlite3.connect('bakery.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()

#home page logic
@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" in session:
        return render_template("recipes.html", title = "Home", user_id = session["user_id"])
    else:
        return render_template("recipes.html", title = "Home")
    
#Bread engine logic
@app.route("/bread_engine", methods=["GET", "POST"])
def bread():
    if request.method != 'POST':
        db_ingredients = c.execute("SELECT * FROM ingredients")
        return render_template('bread_engine.html', ingredients = db_ingredients)

    #update ingredient to a dict with their name and weight in grammsso that they can be added to the recipe
    else:
        recipe = request.form["name"]
        description = request.form["description"]
        form_ingredients = request.form.to_dict()

        #removing elements not needed for the recipe.
        rem_result = ['name', 'description', 'ingredient']
        for element in rem_result:
            del form_ingredients[element]

        #adding the recipe into the database
        c.execute("INSERT INTO recipes (name, description, user_id) VALUES (?,?,?)", (recipe, description, session["user_id"]))

        #getting the recipe id from the db
        recipe_id = c.lastrowid
        
        #creating tuple to insert ingredient_recipes in the db
        data_to_insert = []
        for ingredient in form_ingredients.items():
            ingredient += (recipe_id,)
            data_to_insert.append(ingredient)
        print(data_to_insert)
        #adding ingredients in the junction table
        c.executemany("INSERT INTO recipe_ingredients (ingredient_id, weight, recipe_id) VALUES (?,?,?)", data_to_insert)
        
        #commit recipe and ingredients to DB
        conn.commit()
        return redirect('/')

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

