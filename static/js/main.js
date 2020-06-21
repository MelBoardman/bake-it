
  document.addEventListener('DOMContentLoaded', function() {
     var elems = document.querySelectorAll('select');
     var instances = M.FormSelect.init(elems);
   });


const skill_1_option = document.querySelector("#skill_1");
const skill_2_option = document.querySelector("#skill_2");
const skill_3_option = document.querySelector("#skill_3");
const skill_4_option = document.querySelector("#skill_4");
 
// Taken from http://www.randomsnippets.com/2008/02/21/how-to-dynamically-add-form-elements-via-javascript/
var ingredientCounter = 1;
var ingredientLimit = 20;
function addIngredients(divName){
     if (ingredientCounter == ingredientLimit)  {
          alert("You have reached the limit of adding " + ingredientCounter + " ingredients");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Ingredient " + (ingredientCounter + 1) + " <br><input type='text' name='myIngredients[]'>";
          document.getElementById(divName).appendChild(newdiv);
          ingredientCounter++;
     }
}

var prepCounter = 1;
var prepLimit = 20;
function addPrepSteps(divName){
     if (prepCounter == prepLimit)  {
          alert("You have reached the limit of adding " + prepCounter + " preparation steps");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Preparation Step " + (prepCounter + 1) + " <br><input type='text' name='myPrepSteps[]'>";
          document.getElementById(divName).appendChild(newdiv);
          ingredientCounter++;
     }
}

