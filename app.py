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
        user_recipes = c.execute("SELECT r.id, r.name as recipe_name, r.description FROM recipes r WHERE r.user_id = ?;", (session["user_id"],)).fetchall()
        recipes_ingredients = c.execute("""
                SELECT r.id as recipe_id, i.name, ri.weight FROM recipes r 
                INNER JOIN recipe_ingredients ri on ri.recipe_id = r.id 
                INNER JOIN ingredients i on i.id = ri.ingredient_id WHERE r.user_id = ?;""", (session["user_id"],)).fetchall()
        return render_template("recipes.html", title = "Home", user_recipes = user_recipes,  recipes_ingredients = recipes_ingredients)
    else:
        return render_template("layout.html", title = "Home")
    
#Bread engine logic
@app.route("/bread_engine", methods=["GET", "POST"])
def bread():
    db_ingredients = c.execute("SELECT * FROM ingredients")
    if request.method != 'POST':
        return render_template('bread_engine.html', ingredients = db_ingredients)

    #update ingredient to a dict with their name and weight in grammsso that they can be added to the recipe
    else:
        recipe = request.form["name"]
        description = request.form["description"]
        form_ingredients = request.form.to_dict()

        #form security
        if (recipe == '' or description == ''):
            flash('You must enter a recipe name and a description to continue.', 'info')
            return render_template('bread_engine.html', ingredients = db_ingredients, recipe = recipe, description = description)
                
        for element in form_ingredients:
            print(element)
            if form_ingredients[element] == '':
                flash('You cannot add an ingredient without a weight. Please try again', 'info')
                return render_template('bread_engine.html', ingredients = db_ingredients, recipe = recipe, description = description)

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
        #adding ingredients in the junction table
        c.executemany("INSERT INTO recipe_ingredients (ingredient_id, weight, recipe_id) VALUES (?,?,?)", data_to_insert)
        
        #commit recipe and ingredients to DB
        conn.commit()
        flash('Username already taken, please try another.', 'info')
        return redirect('/')

#baker % logic
@app.route("/baker_per", methods=["GET", "POST"])
def baker_per():
    if request.method != 'POST':
        return redirect("/")
    else:
        #get id from recipe to display
        recipe_id = request.form["recipe_id"]
        # #get the ingredients & info from that recipe
        recipe_info = c.execute("SELECT r.id, r.name as recipe_name, r.description FROM recipes r WHERE r.id = ?;", (recipe_id,)).fetchone()

        #show all that beauty to my incredible user using function declared at the bottom of the file
        return render_template("baker_per.html", recipe_info = recipe_info, recipes_ingredients = bread_calculator(recipe_id, 'ingredients'), baker_per = bread_calculator(recipe_id, 'baker_per'), total_flour = bread_calculator(recipe_id, 'total_flour'), total_weight = bread_calculator(recipe_id, 'dough_weight'))

#recipe adaptor logic
@app.route("/adapt", methods=['GET','POST'])
def adapt():
    if request.method != 'POST':
        return redirect("/")
    else:
        #get recipe info
        recipe_id = request.form["recipe_id"]
        recipe_info = c.execute("SELECT r.id, r.name as recipe_name, r.description FROM recipes r WHERE r.id = ?;", (recipe_id,)).fetchone()

        #get final dough weight
        new_total_weight = 0
        adapted_flour_weight = request.form["new_weight"]
        #compute change in ingredient, add it to a new recipe array
        adapted_recipe = []
        new_flour_weight = float(adapted_flour_weight) / (bread_calculator(recipe_id, 'total_per')/100.0)
        baker_per = bread_calculator(recipe_id, 'baker_per')
        for ingredient in baker_per:
            ingredient_dic = {}
            ingredient_dic['name'] = ingredient['name']
            ingredient_dic['weight'] = '{:.2f}'.format((float(ingredient['percentage'])/100) * float(new_flour_weight))
            new_total_weight += float(ingredient_dic['weight'])
            adapted_recipe.append(ingredient_dic)

        return render_template("adapt.html", recipe_info = recipe_info, recipes_ingredients = bread_calculator(recipe_id, 'ingredients'), baker_per = bread_calculator(recipe_id, 'baker_per'), total_flour = bread_calculator(recipe_id, 'total_flour'), total_weight = bread_calculator(recipe_id, 'dough_weight'), adapted_recipe = adapted_recipe, new_total_weight = round(new_total_weight))
        


#delete recipe logic
@app.route("/delete", methods=["GET", "POST"])
def delete_recipe():
    if request.method != 'POST':
        return redirect("/")
    else:
        #get id from recipe to delete
        recipe_id = request.form["recipe_id"]
        #delete recipe
        c.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        c.execute("DELETE FROM recipe_ingredients WHERE recipe_id =?", (recipe_id,))
        #commit removing the recipe and ingredients from db, inform the user
        conn.commit()
        flash("Recipe was deleted successfully", "info")
        return redirect("/")


#view logs logic
@app.route("/recipe_logs", methods=["GET","POST"])
def view_logs():
    if request.method != 'POST':
        user_id = session['user_id']
        #recipe_logs = c.
        return render_template('recipe_logs.html')
    else:
        recipe_id = request.form['recipe_id']
        recipe_info = c.execute("SELECT r.id, r.name as recipe_name, r.description FROM recipes r WHERE r.id = ?;", (recipe_id,)).fetchone()
        recipe_logs = c.execute("SELECT * FROM recipes_logs WHERE recipe_id = ? ORDER BY date ASC", (recipe_id,))
        return render_template('recipe_logs.html', recipe_logs = recipe_logs, recipe_info = recipe_info)

#add log
@app.route('/add_logs', methods=['GET', 'POST'])
def add_logs():
    if request.method != 'POST':
        return redirect('/')
    else:
        form_log = request.form.to_dict()
        flash('Log added!', 'info')
        return redirect('/recipe_logs')


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

#create calculator to be reused
def bread_calculator(recipe_id, return_value):
    #get general information
    recipes_ingredients = c.execute("""
        SELECT r.id as recipe_id, i.name, ri.weight FROM recipes r 
        INNER JOIN recipe_ingredients ri on ri.recipe_id = r.id 
        INNER JOIN ingredients i on i.id = ri.ingredient_id WHERE r.id = ?;""", (recipe_id,)).fetchall()
    
    #return value = total_flour
    if return_value == 'total_flour':
        total_flour = 0
        for ingredient in recipes_ingredients:
            if ingredient['name'] == "White flour" or ingredient['name'] == "Whole-wheat flour":
                total_flour += ingredient['weight']
        return total_flour

        
    #return value = dough_weight
    if return_value == 'dough_weight':
        total_weight = 0
        for ingredient in recipes_ingredients:
            total_weight += ingredient['weight']
        return total_weight
    
    #return value = ingredients
    if return_value == 'ingredients':
        return recipes_ingredients
    
    #return value = total_per
    if return_value == 'total_per':
        total_per = 0
        total_flour = 0.0
        for ingredient in recipes_ingredients:
            if ingredient['name'] == "White flour" or ingredient['name'] == "Whole-wheat flour":
                total_flour += ingredient['weight']
        for ingredient in recipes_ingredients:
            total_per += (ingredient['weight']/total_flour)*100
        return total_per
    
    #return value = baker_per
    if return_value == 'baker_per':
        baker_per= []
        total_flour = 0
        #get the total amount of flour
        for ingredient in recipes_ingredients:
            if ingredient['name'] == "White flour" or ingredient['name'] == "Whole-wheat flour":
                total_flour += ingredient['weight']

        #generate baker percentages
        for ingredient in recipes_ingredients:
            ingredient_dic = {}
            ingredient_dic["name"] = ingredient["name"] 
            ingredient_dic["percentage"] = '{:.2f}'.format((ingredient['weight']/total_flour)*100)
            baker_per.append(ingredient_dic)
        return baker_per


#launch the app
if __name__ == "__main__":
    app.run()


