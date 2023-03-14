from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("recipes.html", title = "CS50 Bakery")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template('register.html')
    
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('recipes.html')

@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template('recipes.html')

if __name__ == "__main__":
    app.run()

