# CS50 Bakery
#### Video Demo:  <https://youtu.be/ADK67_a0QFY>
#### Description:

This project is a web app that allows users to store bread recipes in grams. 
When adding a recipe to the database, baker's percentage will be automatically generated for the users. Users will also be able to change the yield of the recipe to obtain a precise final dough weight. The final feature for this release is the ability to add logs to particular recipes. Information contained in logs include date, bulk fermentation time, proofing time, temperature and comments. 

Please note that although passwords are encrypted, you should not put any sensitive information in this application. No email addresses are required to log-in. This feature is only there so that you can access your recipes. 

## Templates
The application interface is rendered using HTML, CSS, JavaScript as well as Flask and Jinja. No CSS frameworks were used for this project. Some component and were created thank to tutorials online and the occasional chatGPT question.

## Static
Contains the stylesheet, the background image and script file for rendering the web application UI.

## App.py

This programs uses HTML, CSS, JavaScript and Flask to render the content to the users. SQLite3 is used in cunjunction with row factory to communicate between the front-end and the backend. The following have been implemented in this release:

### Register, login, logout
Allows the users to register and login. Passwords are encrypted with werkzeug. Basic checks are also made. For instance, usernames cannot be duplicated and password must be confirmed and match.
Once logged-in, the app uses the built-in Flask feature "session[]" to store the users' id and let users access their informations and recipes. Upon login out, session is cleared with all users information. 
**Used with login.html, register.html and layout.html to render the front end.** 

### bread_calculator function
This function is the one reused the major features of the app. It takes two arguments: the recipe_id and the return value desired. Here are its feature-set:
- Returns the total weight of the flour in the recipe
- Returns the final dough weight of the recipe
- Generates baker's percentage using sqlite3 rowfactory and adding it into a python dictionnary so that it can be easily shown to the users using Jinja. 
    - The function can also compute the total percentage of a recipe. That is, the sum of all the ingredients expressed as a percentage of the flour weight. This allows to scale the recipe up or down
- Returns a dictionnary list of ingredients so that any recipes can be displayed to the users.

### Home page
This function returns an empty home page by default. If users are logged in, it instead queries the database to get the users' recipes. It uses **layout.hmlt** as well as **recipes.html** (which simply extends layout.html) to display the content front-end wise. Regarding the backend, the home() function gets called and most other features of the app redirect users toward this homepage.

### Bread engine logic
The function used is called bread(). Its purpose in life is to get the information inserted by users in the form present in **bread_engine.html**. 

To ensure clean data is inserted in the DB, all fields that users insert must be filled. A verification is done before letting users insert data in the DB. Information is injected as follows:
1. Recipe name, description are taken from the form
2. Using the **request.form.to_dict()** Flask method, all of the fields are then retrieved from the form. 
3. Recipe name and description are then taken off the list obtained in step 2 so that only the ingredients inserted by users remain. **Please note** that request.form.to_dict is used because it is impossible to predict in advance how many fields the form will contain. More on that in the frontend explanation. 
4. Recipe name, description and ingredients are then converted into a tupple so that they can be inserted using sqlite3 for python.

**Bread engine front-end**

Front-end for this html page is mainly generated with javaScript and Flask. Firstly, a query retrieves ingredients from the SQLite db to display a list of option to the users. They can then select an ingredient and add it. 

Through javaScript, an input form gets automatically inserted in the HTML page with the necessary information to be retrieved by the server. Added ingredients can also be discarded from the form. If that is the case, they go back to the option menu so that the users are still able to change their mind. 

### Baker's percentages logic
Using the baker_per() and the bread_calculator function, this page displays the recipe users have chosen as well as the recipe converted to baker's percentages. To do so, all ingredients weight corresponding to the recipe are retrieved from the recipe_ingredients table. The process is then as follows:
1. List all ingredients that are flour
2. Add all flour wieght. This is now the basis on which all other ingredients will be divided.
3. For each ingredient, divide the ingredient weight by the total weight of the flour. Each resulting number is added to a dictionnary that contains as a key the ingredient name and as a value the ingredient percentage. Each dictionnary is then appended to a list so that it can be displayed to the users.


This information is displayed on the **baker_per.html** page. This page also contains a form that allows users to adapt the final yield of the dough. 

### Recipe adaptor logic
Using information retrieved from the **bread_calculator** function, the users are allowed to input a final dough weight into a HTML form.  They are then redirected towards the **adapt.html** web page which extends the **baker_per.html** page. The recipe adaptation is computed as follows:

1. Retrieve all ingredients from the selected recipe.
2. Using the bread_calculator function, retrieve the baking percentages for the recipe.
3. Add all the percentages together. This will be the basis to compute the new flour weight. 
4. Divide the desired dough weight inputed by the users by the sum of all percentages computed in step 3. This is now the new flour weight.
5. For each remaining ingredients, multiply the flour weight by the ingredient baker's percentage. This now gives the weight in grams of the ingredient in the adapted recipe. 

### Delete recipe logic
Using the delete option on the **recipes.html** page, users are allowed to remove a recipe, as well as all related recipe ingredients and recipe logs from the database. Users are then redirected to the home page.

### View recipe logs 
From the **recipes.html** page, users can see and insert logs for recipes using the "Logs" option present on each recipe. This redirects them to the **user_logs.html** page. 

From there, users can either consult the logs that were previously inserted or add new ones. To add new logs, a HTML form is displayed on demand using javaScript. When inserting logs, the server verifies that all the information required from the users was added to the form. If that is not the case, the users are redirected to the log page where they can try again. Otherwise, users are redirected to the homepage. 

### View general logs
Using the **user_logs.html** page, users can see all logs they have added to their recipes. Logs are sorted by date from the latest to the earliest. 

## Bakery.db
SQLite3 database designed for the application. Contains the following table:
- Users
    - Contains all information about users
- Ingredients 
    - Contains ingredient list. Can be updated in the future to better reflect home baker reality. It is queried when users wish to add a new recipe in the database.
- Recipes
    - Contain all information related to a user's recipe. Namely, recipe name, unique identifier, recipe owner and recipe description.
- Recipe_ingredients
    - Junction table that allows a one-to-many relationship between recipes and ingredients. It contains the recipe id, the ingredient weight as well as the ingredient id. 
- Recipe_logs
    - Points to the recipes table. Allows users to add further information about their recipes. Information include bulk fermentation time, proofing time, temperature and comments. 