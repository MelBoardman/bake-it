import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from os import path
if path.exists("env.py"):
  import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'bake-it'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    return render_template("all_recipes.html", cat_list = list(mongo.db.recipe_category.find()), recipes=mongo.db.recipes.find())

@app.route("/display_recipe/<recipe_id>")
def display_recipe(recipe_id):
  
  return render_template("recipe.html", cat_list = list(mongo.db.recipe_category.find()),recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
