import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import datetime

from os import path
if path.exists("env.py"):
  import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'bake-it'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)
 
@app.route("/")
@app.route("/home")
def home():
  if 'username' in session:
    members = mongo.db.members
    member = members.find_one({'username' : session['username']})
    if member['member_type'] == 'admin':
      return render_template("index.html", 
                              admin = True, 
                              logged_in = True, 
                              message ='You are logged in as ' + session['username'],
                              recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                              cat_list = list(mongo.db.recipe_category.find()))
    return render_template("index.html", 
                            logged_in = True, 
                            message ='You are logged in as ' + session['username'],
                            recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                            cat_list = list(mongo.db.recipe_category.find()))
  return render_template("index.html",
                          recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                          cat_list = list(mongo.db.recipe_category.find()))

@app.route("/log_in", methods=['POST', 'GET'])
def log_in():
  if request.method == 'POST':
    members = mongo.db.members
    login_member = members.find_one({'username' : request.form['username']})
    if login_member:

      if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_member['password'].encode('utf-8')) == login_member['password'].encode('utf-8'):
        # set session user id
        session['username'] = request.form['username']
        if login_member['member_type'] == 'admin':
          return redirect(url_for('admin_page', 
                                  username =session['username'], 
                                  logged_in = True, 
                                  admin = True))
        
        return redirect(url_for('my_recipes', 
                                username =session['username'], 
                                logged_in = True)) 
    
    return render_template("log_in.html", 
                            log_on_fail = True, 
                            message = 'Invalid username/password combination')
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
            return redirect(url_for('my_recipes', 
                                    username =session['username'], 
                                    logged_in = True)) 

        return render_template("sign_up.html", 
                              username_fail = True, 
                              message = "That username already exists!")

  return render_template("sign_up.html")

@app.route("/my_recipes/<username>")
def my_recipes(username):
  members = mongo.db.members
  member = members.find_one({'username' : session['username']})
  if member['member_type'] == 'admin':
    return render_template("my_recipes.html", 
                          admin = True, 
                          logged_in = True, 
                          username =session['username'], 
                          cat_list = list(mongo.db.recipe_category.find()), 
                          recipes=mongo.db.recipes.find({"added_by": session['username']}))

  return render_template("my_recipes.html",
                        logged_in = True, 
                        username =session['username'], 
                        cat_list = list(mongo.db.recipe_category.find()), 
                        recipes=mongo.db.recipes.find({"added_by": session['username']}))

@app.route("/admin_page/<username>")
def admin_page(username):
  return render_template("admin.html", 
                          admin = True, 
                          logged_in = True, 
                          username =session['username'], 
                          categories = (mongo.db.recipe_category.find()), 
                          recipes=mongo.db.recipes.find())

@app.route("/add_category")
def add_category():
  return render_template("add_category.html", 
                          admin = True, 
                          logged_in = True, 
                          username =session['username'], 
                          categories = (mongo.db.recipe_category.find()))

@app.route("/insert_category", methods=['POST', 'GET'])
def insert_category():
  categories = mongo.db.recipe_category
  categories.insert_one(
    {
        'category_name': request.form.get('category_name'),
        'ad_links': {'ad_product_name': request.form.get('ad_product_name'),
                      'ad_product_description': request.form.get('ad_product_description'),
                      'ad_product_link': request.form.get('ad_product_link'),
                      'ad_product_image': request.form.get('ad_product_image')
    }})
  return redirect(url_for('admin_page', 
                  username =session['username'], 
                  logged_in = True, 
                  admin = True))

@app.route("/edit_category/<category_id>")
def edit_category(category_id):
  return render_template("edit_category.html", 
                          admin = True, 
                          logged_in = True, 
                          category = mongo.db.recipe_category.find_one({"_id": ObjectId(category_id)}))

@app.route("/update_category/<category_id>", methods=['POST', 'GET'])
def update_category(category_id):
  categories = mongo.db.recipe_category
  categories.update({'_id': ObjectId(category_id)},
    {
        'category_name': request.form.get('category_name'),
        'ad_links': {'ad_product_name': request.form.get('ad_product_name'),
                      'ad_product_description': request.form.get('ad_product_description'),
                      'ad_product_link': request.form.get('ad_product_link'),
                      'ad_product_image': request.form.get('ad_product_image')
    }})
  return redirect(url_for('admin_page', 
                          username =session['username'], 
                          logged_in = True, 
                          admin = True))

@app.route("/delete_category/<category_id>")
def delete_category(category_id):
  mongo.db.recipe_category.remove({'_id': ObjectId(category_id)})
  return redirect(url_for('admin_page', 
                          username =session['username'], 
                          logged_in = True, 
                          admin = True))

@app.route("/get_recipes")
def get_recipes():
  if 'username' in session:
    members = mongo.db.members
    member = members.find_one({'username' : session['username']})
    if member['member_type'] == 'admin':
      return render_template("all_recipes.html", 
                              logged_in = True, 
                              admin = True, 
                              cat_list = list(mongo.db.recipe_category.find()), 
                              recipes=mongo.db.recipes.find())

    return render_template("all_recipes.html", 
                            logged_in = True, 
                            cat_list = list(mongo.db.recipe_category.find()), 
                            recipes=mongo.db.recipes.find())

  return render_template("all_recipes.html", 
                          logged_in = False, 
                          cat_list = list(mongo.db.recipe_category.find()), 
                          recipes=mongo.db.recipes.find())  

@app.route("/display_recipe/<recipe_id>")
def display_recipe(recipe_id):
  if 'username' in session:
    members = mongo.db.members
    member = members.find_one({'username' : session['username']})
    if member['member_type'] == 'admin':
      return render_template("recipe.html", 
                              admin = True, 
                              logged_in = True, 
                              cat_list = list(mongo.db.recipe_category.find()),
                              recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

    return render_template("recipe.html", 
                            logged_in = True, 
                            cat_list = list(mongo.db.recipe_category.find()),
                            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

  return render_template("recipe.html", 
                          cat_list = list(mongo.db.recipe_category.find()),
                          recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

@app.route("/add_recipe")
def add_recipe():
  members = mongo.db.members
  member = members.find_one({'username' : session['username']})
  if member['member_type'] == 'admin':
    return render_template("add_recipe.html", 
                            admin = True, logged_in = True, 
                            categories = mongo.db.recipe_category.find())

  return render_template("add_recipe.html", 
                          logged_in = True,  
                          categories = mongo.db.recipe_category.find())

@app.route("/insert_recipe", methods=['POST', 'GET'])
def insert_recipe():
  now = datetime.datetime.now()
  recipes = mongo.db.recipes
  recipes.insert_one(
    {
        'recipe_name': request.form.get('recipe_name'),
        'added_by': session['username'],
        'description': request.form.get('recipe_description'),
        'category_name': request.form.get('category_name'),
        'prep_time': request.form.get('prep_time'),
        'cook_time': request.form.get('cook_time'),
        'ingredients': request.form.getlist('myIngredients[]'),
        'preparation_steps': request.form.getlist('myPrepSteps[]'),
        'skill_level': int(request.form.get('skill')),
        'date_added': now,
        'image': request.form.get('recipe_image')
    })
  return redirect(url_for('get_recipes'))

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
  members = mongo.db.members
  member = members.find_one({'username' : session['username']})
  if member['member_type'] == 'admin':
    return render_template("edit_recipe.html", 
                            admin = True, 
                            logged_in = True, 
                            cat_list = list(mongo.db.recipe_category.find()),
                            categories = mongo.db.recipe_category.find(),
                            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

  return render_template("edit_recipe.html", 
                          logged_in = True, 
                          cat_list = list(mongo.db.recipe_category.find()),
                          categories = mongo.db.recipe_category.find(),
                          recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
  now = datetime.datetime.now()
  recipes = mongo.db.recipes
  recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name': request.form.get('recipe_name'),
        'added_by': session['username'],
        'description': request.form.get('recipe_description'),
        'category_name': request.form.get('category_name'),
        'prep_time': request.form.get('prep_time'),
        'cook_time': request.form.get('cook_time'),
        'ingredients': request.form.getlist('myIngredients[]'),
        'preparation_steps': request.form.getlist('myPrepSteps[]'),
        'skill_level': int(request.form.get('skill')),
        'date_added': now,
        'image': request.form.get('recipe_image')
    })
  return redirect(url_for('get_recipes'))

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.secret_key = os.environ.get('SECRET_KEY')
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'))
