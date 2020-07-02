# Milestone Project 3 - Code Institute Full Stack Developer Course

## BAKE IT!

### Introduction

A website that is used for accessing and sharing baking recipes. Baking is quite popular at the moment with the great British Bake off and people seem to be passing time in lockdown by rediscovering baking. 

The site owners goal is to share and collect recipes and to advertise cooking equipment.

I have decided to advertise the brand ‘Pyrex’. They are a well-established brand and are known for their hard wearing well-designed products that can be found in most kitchens. https://www.pyrexuk.com/collections/bakeware

The main priorities for the site are accessing recipes, sharing recipes and advertising bakeware.

## UX
 
I wanted to produce a simple easy to use website where people can easily share and view baking recipes. As there are lots of different images on the recipe cards I decided to keep the background simple and went for a simple gingham style as to give the feel of a country kitchen table cloth. I selected a teal theme as it is one of my favorite colours and I think it fits with the style I am aiming for.

I chose to use the materialize framework to produce the site. I liked the fonts and the simple / clean feel.  This allowed me to focus my attention on the database schema and the back end code.

Looking at the Pyrex bakeware products I decided that I would link 1 product to each of the baking categories. i.e. 'Cupcake baking tray' to 'cupcakes and muffins' category. This also makes it easier for the Admin to add and alter products and categories in one form making the Admin user experience simple, straightforward and quick. After gathering my thoughts and initial ideas I started to develop a list of user stories.

### User Stories:
I have determined that there are 3 types of user:
1.	New Visitor:

    A non-member visiting the site for the first time. 

2.	A Member

    Likes to browse the site. Looks for the recently added recipes and Likes to share their recipes.

3.	Site Owner / Admin
	
    Can add recipes and update and delete any recipes added to the site. Updates recipe categories. Updates Advertisements. 

There will be user stories for each user type and there will also be user stories that are applicable to all users. Such as UX i.e. recipe contents and layout.  Imagery etc… In these instances, I shall refer to them as a ‘User’.

1.	As a new visitor I want to understand the purpose of the site
2.	As a new visitor I want to browse baking recipes.
3.	As a new visitor I want to learn how to become a member.
4.	As a new visitor I want the Member sign up process to be simple.
5.	As a member I want to share one of my recipes.
6.	As a member I want to see what new recipes have been added recently.
7.  As a member I want to be able to update and delete recipes that I have previously added.
8.	As an Admin I want to be able to create, update and delete the baking recipe categories.
9.	As an Admin I want to be able to update and delete recipes on the site. 
10.	As an Admin I want to be able to modify the links to the bake ware ads.
11. As a user I want to be able to view recipes based on the recipe category.
12.	As a user I want to be able to see the name of a recipe. E.g. Chocoholics Muffins
13.	As a user I want to see the description of a recipe. E.g. Delicious chocolate muffins with white and milk chocolate chips and chocolate topping.
14.	As a user I would like to see the preparation and cooking time for each recipe.
15.	As a user I want to see the level of skill required to complete each recipe.
16.	As a user I want to see the ingredients required for the recipe.
17.	As a user I want to see the instructions on how to complete the recipe.
18.	As a user I want to see an image on the recipe page.
19.	As a user I want to see links to good quality bake ware to allow me to improve my baking.
20.	As a user I want the site to be fun to look at.
21.	As a user I want the site to be easy to navigate.

After determining the user stories I put together some basic wireframes.   

Click here for [Wireframes](./docs/MS3Wireframes.pdf).

I then spent time working out how to structure the data needed. 

I decided I required 3 collections in my database. 
1. members - I wanted this to be simple as I have limited experience in security issues with passwords and email addresses etc.. So I decided to just use a username and password. The collection also takes a users member_type. This is always member. I manually changed one user to be an Admin.

2. recipe_category - This includes the category name. i.e. Cupcakes and the product information that will be advertised when this recipe category is included in a recipe. 

3. recipes - This includes all the information for the recipe, Name, description, prep and cook times, skill level, ingredients, preparation steps and a link to an image. I also included a data added and date updated. This was to allow the recipes to be displayed so that the most recently added is shown first.  

Click here for [Database Schema](./docs/database_schema.pdf).



## Features

### Navbar:  Materialize nav bar
-    The Nav bar has links to the various pages and the options are modified dependant on if someone is logged in and if they are an admin. Once a member is logged on the 'Log in' link is changed to 'My Recipes'. If an Admin is logged in the Admin link is also added. 

### Homepage: index.html
-   Description on the homepage to allow new visitors to quickly understand the purpose of the site.
-   Link to a Sign up page that allows new visitors to be easily become members.
-   Button link to Log In page so members can log in
-   If a user is logged in the Text is altered slightly and there is a message "You are logged in as..."
-   Button link to All recipes to allow all users to access all the recipes from one click from the Homepage. 
-   Display the latest recipes that have been added so that returning visitors can quickly see and any new exciting recipes.

### Sign Up Page: sign_up.html
-   Simple Sign up procedure. Using only a Username and password. i.e. limiting personal data and encourage people to sign up.
-   Link to log in page if you realise you are an existing user.

### Log In Page: log_in.html
-   log in page takes the username and password. When a user is successfully logged in it returns them to the homepage.

### Recipes page: all_recipes.html
- Displays all recipes on cards with most recent first. 
- Button to filter by recipe category.
- Button to add a new recipe. 

### My Recipes page: all_recipes.html
- This uses the same html page as all recipes and the functionality is the same. However only recipes added by the user that is currently logged in are displayed. This page is only accessible when there is a user in session.

### Recipe page: recipe.html
-   If the image or the 'bake it' button on a recipe card is selected from any page the user is taken to the recipe page where the recipe is displayed.

### Add Recipe page: add_recipe.html
-   The add a recipe button can be pressed in the recipes or my recipes pages. This brings the user to the add a recipe page that contains the form that collects the data for the database. 

### Edit Recipe page: edit_recipe.html
-   An Admin can edit all recipes. A member can edit recipes that they have added. The edit option can be found on the recipe card on any page that the card is displayed on.
-   Clicking the EDIT button takes the user to the edit recipe page where the information for the recipe is displayed as it was in the entry form. All the current data is populated and can be edited. 

### Admin page: admin.html
-   If an admin user is logged in there is an additional link on the nav bar for the Admin page. 
-   The admin page displays the recipe categories on cards. They show the category name and the name of the product that is advertised in the recipes that that category is used.
- there is also a button to add new categories.

### Add a recipe category: add_category.html
-   When Add a category button is selected from the Admin page. The Add a recipe category form is displayed. The Admin can enter the category name and the product information they wish to advertise when this category is selected. 

### Edit a category: edit_category.html
- This can be accessed by selecting the edit button on the category cards in the Admin page. 
- This takes the admin to the same form as shown in the add a category page. The form is populated and all items can be edited.


### Features Left to Implement

- Add a filter to allow recipes to be filtered by skill level.
- Add a link to 'Bake its favorite Pyrex products' and a page that lists them all using the ad data populated in the categories database. 
- Add feature to Admin Tools: allow Admins to change other users member_type to Admin. 

## Technologies Used

- HTML - https://www.w3schools.com/whatis/whatis_html.asp
- CSS, 
- JS, 
- JQUERY, 
- PYTHON - FLASK, 
- MONGO DB - https://cloud.mongodb.com 
- MATERIALIZE 1.0 - https://materializecss.com/about.html

## Testing

For this project I completed a lot of manual testing and cross checking what had been added to the database in Mongo throughout the development of each feature. I then completed some comprehensive manual testing laid out in the following spreadsheet:

Click here for [Testing Spreadsheet](./docs/manual_testing.pdf).

As I have used the Materialize framework there is limited bespoke JS that in this project and this has been thoroughly tested manually therefore I have not completed any Jasmine testing.

I discussed python unit testing with my mentor and I managed to create a few simple tests in the test.py. However this is not complete and I hope to gain more experience in this in the next module. 

Throughout development I have also be checking each feature with chrome developer tools looking at different screen sizes and using my own devices. 

I also sent links to the site to many family and friends and feel I have completed enough validation to believe the site functions as intended. Aside from a couple of issues in IE highlighted in the test spreadsheet.


## Deployment

I have developed this project in VSCode. In order to set up a virtual environment I followed this: https://docs.python.org/3/library/venv.html

To deploy Bake-it to Heroku:

-   A requirements.txt is needed. This is created by using the following command in the terminal : pip freeze > requirements.txt.
-   A Procfile is also required. This created by using the following command in the terminal: echo web: python app.py > Procfile
-   Ensure the above files are commited and pushed to the repository in git hub. (git add .)(git commit -m "....")(git push)
-   Next the app must be created on the heroku website: https://dashboard.heroku.com/ by selecting New on the dashboard. Then create a name: bake-it and set the region to Europe.
-   On the HeroKu dashboard select the app (bake-it) selct 'deploy', 'deployment method' and select github. 
-   Link the (bake-it) app to the correct repository in github. 
-   I have developed this project in VSCode. I have used a virtual environment. The env.py file holds the environment variables. This does not get commited to github and therefore these variables must be added to the Heroku config vars.
-   Select 'settings' then 'reveal Config Vars' then set the config vars as follows:
-       Key: DEBUG  value: False
-       Key: IP     value:  0.0.0.0
-       Key: MONGO_URI value: mongodb+srv://.......................
-       Key:PORT    value:5000
-       Key:SECRET_KEY  value: its a secret
-   From the Deploy tab you can select 'deploy branch' ensuring the master branch is selected, from the manual deploy section or it wait for the next git push when it will automatically be deployed.


## Credits

### Content

To work out how to do a simple log in I came across this tutorial on youtube.com  https://www.youtube.com/watch?v=vVx1737auSE I used this to base my sign up and log in functionality. https://github.com/PrettyPrinted/mongodb-user-login

For the 'Add recipe' page it was necessary to dynamically add form fields. I wasn't sure how to achieve this and a google search led me to this page:  http://www.randomsnippets.com/2008/02/21/how-to-dynamically-add-form-elements-via-javascript/ This code achieved what I wanted and is included in my main.js file.

### Media

https://www.pyrexuk.com/collections/bakeware



### Acknowledgements

During development I used online resources to help with issues I came across:

https://www.w3schools.com/
https://stackoverflow.com/

My Mentor briefly talked me thought unit testing and i found this: https://code-maven.com/slides/python-programming/flask-testing  and this https://blogthetech.com/testing-flask-applications-using-unittest-in-python/#Routing_Tests and from this I managed to put together some basic python route tests.

I would also like to thank my Mentor: Ignatius Ukwuoma for the support.


