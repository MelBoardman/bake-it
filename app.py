import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

from os import path
if path.exists("env.py"):
  import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'bake-it'
app.config["MONGO_URI"] = os.getenv('MONGO_URI','mongodb://localhost')

mongo = PyMongo(app)
 
@app.route("/")
@app.route("/home")
def home():
  if 'username' in session:
        return render_template("index.html", logged_in = True, message ='You are logged in as ' + session['username'])
  return render_template("index.html")

@app.route("/log_in", methods=['POST', 'GET'])
def log_in():
  if request.method == 'POST':
    members = mongo.db.members
    login_member = members.find_one({'username' : request.form['username']})
    if login_member:

      if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_member['password'].encode('utf-8')) == login_member['password'].encode('utf-8'):
        # set session user id
        session['username'] = request.form['username']
        return redirect(url_for('my_recipes', username =session['username'])) 
    
    return render_template("log_in.html", log_on_fail = True, message = 'Invalid username/password combination')
  return render_template("log_in.html")

# sign up page used to register new member
@app.route("/sign_up", methods=['POST', 'GET'])
def sign_up():
  # first check to see if username already exists
  if request.method == 'POST':
        members = mongo.db.members
        existing_member = members.find_one({'username' : request.form['username']})

        if existing_member is None:
            # encrypt password
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            # make password a string in mongo
            hashpass = str(hashpass, encoding='utf-8', errors='strict')
            # add new member to mongodb
            members.insert({'username' : request.form['username'], 'password' : hashpass, 'member_type' :'member'})
            # set session user id
            session['username'] = request.form['username']
            return redirect(url_for('my_recipes', username =session['username'])) 
        return render_template("sign_up.html", username_fail = True, message = "That username already exists!")
  return render_template("sign_up.html")

@app.route("/my_recipes/<username>")
def my_recipes(username):
    return render_template("my_recipes.html", cat_list = list(mongo.db.recipe_category.find()), recipes=mongo.db.recipes.find())

@app.route("/get_recipes")
def get_recipes():
    return render_template("all_recipes.html", cat_list = list(mongo.db.recipe_category.find()), recipes=mongo.db.recipes.find())

@app.route("/display_recipe/<recipe_id>")
def display_recipe(recipe_id):
  return render_template("recipe.html", cat_list = list(mongo.db.recipe_category.find()),recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

@app.route("/add_recipe")
def add_recipe():
  return render_template("add_recipe.html", categories = mongo.db.recipe_category.find())

@app.route("/insert_recipe", methods=['POST', 'GET'])
def insert_recipe():
  recipes = mongo.db.recipes
  recipes.insert_one(
    {
        'recipe_name': request.form.get('recipe_name'),
        'added_by': session['username'],
        'description': request.form.get('recipe_description'),
        'category_id': int(request.form.get('category_name')),
        'prep_time': request.form.get('prep_time'),
        'cook_time': request.form.get('cook_time'),
        'ingredients': request.form.getlist('myIngredients[]'),
        'preparation_steps': request.form.getlist('myPrepSteps[]'),
        'skill_level': request.form.get('skill'),
        # 'date_added': ,
        'image': request.form.get('recipe_image')
    })
  return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
