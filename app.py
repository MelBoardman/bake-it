import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import datetime
import unittest

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
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    admin_status = bool(member['member_type'] == 'admin')
  else:
    admin_status = False
    user = ""
  return render_template("index.html", 
                              admin = admin_status, 
                              logged_in = logged_in_status, 
                              message ='You are logged in as ' + user,
                              recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                              cat_list = list(mongo.db.recipe_category.find()))

# Log in page
@app.route("/log_in", methods=['POST', 'GET'])
def log_in():
  if request.method == 'POST':
    members = mongo.db.members
    login_member = members.find_one({'username' : request.form['username']})
    hash_p = bcrypt.hashpw(request.form['password'].encode('utf-8'), login_member['password'].encode('utf-8'))
    if login_member:
      if hash_p == login_member['password'].encode('utf-8'):
        # log in success set session user id
        session['username'] = request.form['username']
        admin_status = bool(login_member['member_type'] == 'admin')
        return redirect(url_for('home', 
                                  username =session['username'], 
                                  logged_in = True, 
                                  admin = admin_status))  
    # log in fail
    return render_template("log_in.html", 
                            log_on_fail = True, 
                            message = 'Invalid username/password combination')
  # route to login page
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
            return redirect(url_for('home', 
                                    username =session['username'], 
                                    logged_in = True)) 

        return render_template("sign_up.html", 
                              username_fail = True, 
                              message = "That username already exists!")

  return render_template("sign_up.html")

# route to all_recipes.html filtered on to recipes added by the user logged in.
@app.route("/my_recipes/<username>")
def my_recipes(username):
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    admin_status = bool(member['member_type'] == 'admin')
  else:
    admin_status = False
    user = ""
  return render_template("all_recipes.html",
                          my_reps = True, 
                          admin = admin_status, 
                          logged_in = logged_in_status, 
                          username =user, 
                          cat_list = list(mongo.db.recipe_category.find()), 
                          recipes=mongo.db.recipes.find({"added_by": session['username']}).sort('date_added',-1),
                          no_of_recipes=mongo.db.recipes.count({"added_by": session['username']}))

# Admin page only accessible by admin user
@app.route("/admin_page/<username>")
def admin_page(username):
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    if member['member_type'] == 'admin':
      return render_template("admin.html", 
                          admin = True, 
                          logged_in = logged_in_status, 
                          username =session['username'], 
                          categories = (mongo.db.recipe_category.find()), 
                          recipes=mongo.db.recipes.find())
    else:
      admin_status = False
      user = ""
# if not an admin redirect to index.html
  return render_template("index.html", 
                            admin = admin_status, 
                            logged_in = logged_in_status, 
                            message ='You are logged in as ' + user,
                            recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                            cat_list = list(mongo.db.recipe_category.find()))
  
# Add category page is only accessible by admin user
@app.route("/add_category")
def add_category():
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    if member['member_type'] == 'admin':
      return render_template("add_category.html", 
                          admin = True, 
                          logged_in = True, 
                          username =session['username'], 
                          categories = (mongo.db.recipe_category.find()))
    else:
      admin_status = False
      user = ""
# if not an admin redirect to index.html
  return render_template("index.html", 
                            admin = admin_status, 
                            logged_in = logged_in_status, 
                            message ='You are logged in as ' + user,
                            recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                            cat_list = list(mongo.db.recipe_category.find()))

@app.route("/insert_category", methods=['POST'])
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

# Add category page is only accessible by admin user
@app.route("/edit_category/<category_id>")
def edit_category(category_id):
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    if member['member_type'] == 'admin':
      return render_template("edit_category.html", 
                          admin = True, 
                          logged_in = logged_in_status, 
                          category = mongo.db.recipe_category.find_one({"_id": ObjectId(category_id)}))
    else:
      admin_status = False
      user = ""
# if not an admin redirect to index.html
  return render_template("index.html", 
                            admin = admin_status, 
                            logged_in = logged_in_status, 
                            message ='You are logged in as ' + user,
                            recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                            cat_list = list(mongo.db.recipe_category.find()))

@app.route("/update_category/<category_id>", methods=['POST'])
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
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    admin_status = bool(member['member_type'] == 'admin')
  else:
    admin_status = False
    user = ""
  return render_template("all_recipes.html", 
                              logged_in = logged_in_status, 
                              user = user,
                              admin = admin_status, 
                              cat_list = list(mongo.db.recipe_category.find()),  
                              recipes=mongo.db.recipes.find().sort('date_added',-1))

# Filter Recipes by category
@app.route("/recipes_by_category/<cat_name>")
def recipes_by_category(cat_name):
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    admin_status = bool(member['member_type'] == 'admin')
  else:
    admin_status = False
    user = ""
  return render_template("all_recipes.html",
                              cat_name = cat_name,
                              cat_selected = True, 
                              logged_in = logged_in_status, 
                              user = user,
                              admin = admin_status, 
                              cat_list = list(mongo.db.recipe_category.find()), 
                              recipes=mongo.db.recipes.find({"category_name": cat_name}),
                              no_of_recipes_cat=mongo.db.recipes.count({"category_name": cat_name}))

# Filter My Recipes by category
@app.route("/my_recipes_by_category/<cat_name>")
def my_recipes_by_category(cat_name):
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    admin_status = bool(member['member_type'] == 'admin')
  else:
    admin_status = False
    user = ""
  return render_template("all_recipes.html",
                              my_reps = True,
                              cat_name = cat_name,
                              cat_selected = True, 
                              logged_in = logged_in_status, 
                              user = user,
                              admin = admin_status, 
                              cat_list = list(mongo.db.recipe_category.find()), 
                              recipes=mongo.db.recipes.find({"added_by": user,"category_name": cat_name}),
                              no_of_my_recipes_cat=mongo.db.recipes.count({"added_by": user,"category_name": cat_name}))

# Route to recipe.html to display all recipe details and tailored ad.
@app.route("/display_recipe/<recipe_id>")
def display_recipe(recipe_id):
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    admin_status = bool(member['member_type'] == 'admin')
  else:
    admin_status = False
    user = ""
  return render_template("recipe.html", 
                          logged_in = logged_in_status, 
                          user = user,
                          admin = admin_status, 
                          cat_list = list(mongo.db.recipe_category.find()),
                          recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

@app.route("/add_recipe")
def add_recipe():
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    admin_status = bool(member['member_type'] == 'admin')
    return render_template("add_recipe.html", 
                            admin = admin_status, 
                            logged_in = True, 
                            categories = mongo.db.recipe_category.find())
  else:
    admin_status = False
    user = ""
# if not an logged in redirect to index.html
    return render_template("index.html", 
                            admin = admin_status, 
                            logged_in = logged_in_status, 
                            message ='You are logged in as ' + user,
                            recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                            cat_list = list(mongo.db.recipe_category.find()))
 
# Route to insert recipe into the database
@app.route("/insert_recipe", methods=['POST'])
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
  logged_in_status = bool('username' in session)
  if logged_in_status:
    members = mongo.db.members
    user = session['username']
    member = members.find_one({'username' : user})
    admin_status = bool(member['member_type'] == 'admin')
    return render_template("edit_recipe.html", 
                            admin = admin_status, 
                            logged_in = logged_in_status, 
                            cat_list = list(mongo.db.recipe_category.find()),
                            categories = mongo.db.recipe_category.find(),
                            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))
  # if not an logged in redirect to index.html
  return render_template("index.html", 
                            admin = admin_status, 
                            logged_in = logged_in_status, 
                            message ='You are logged in as ' + user,
                            recently_added = mongo.db.recipes.find().sort('date_added',-1).limit(3),
                            cat_list = list(mongo.db.recipe_category.find()))

# route to update recipe in the database
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

# route to delete recipe in the database
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.secret_key = os.environ.get('SECRET_KEY')
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=os.environ.get('DEBUG'))
