document.addEventListener('DOMContentLoaded', function () {
     var elems = document.querySelectorAll('select');
     var instances = M.FormSelect.init(elems);
});

// skill level select
const skill1 = document.querySelector("#skill_1");
const skill2 = document.querySelector("#skill_2");
const skill3 = document.querySelector("#skill_3");
const skill4 = document.querySelector("#skill_4");
const skillLevel = document.querySelector("#skill_level");
const skill = document.querySelector("#skill")
var click = false;
var skillLevelSelected = 0;

skill1.addEventListener('mouseover', (event) => {
     skill1.innerHTML = "radio_button_checked";
});
skill1.addEventListener('mouseout', (event) => {
     if (click == false) {
     skill1.innerHTML = "radio_button_unchecked";
     }
});
skill1.addEventListener('click', (event) => {
     click = true;
     skill.value = 1;
     skill1.innerHTML = "radio_button_checked";
     addSkillLevel(1)
});


skill2.addEventListener('mouseover', (event) => {
     skill1.innerHTML = "radio_button_checked";
     skill2.innerHTML = "radio_button_checked";
});
skill2.addEventListener('mouseout', (event) => {
     if (click == false) {
     skill1.innerHTML = "radio_button_unchecked";
     skill2.innerHTML = "radio_button_unchecked";
     }
});
skill2.addEventListener('click', (event) => {
     click = true;
     skill.value = 2;
     skill1.innerHTML = "radio_button_checked";
     skill2.innerHTML = "radio_button_checked";
     addSkillLevel(2)
});

skill3.addEventListener('mouseover', (event) => {
     skill1.innerHTML = "radio_button_checked";
     skill2.innerHTML = "radio_button_checked";
     skill3.innerHTML = "radio_button_checked";
});
skill3.addEventListener('mouseout', (event) => {
     if (click == false) {
          skill1.innerHTML = "radio_button_unchecked";
          skill2.innerHTML = "radio_button_unchecked";
          skill3.innerHTML = "radio_button_unchecked";
     }
});
skill3.addEventListener('click', (event) => {
     click = true;
     skill.value = 3;
     skill1.innerHTML = "radio_button_checked";
     skill2.innerHTML = "radio_button_checked";
     skill3.innerHTML = "radio_button_checked";
     addSkillLevel(3)
});



skill4.addEventListener('mouseover', (event) => {
     skill1.innerHTML = "radio_button_checked";
     skill2.innerHTML = "radio_button_checked";
     skill3.innerHTML = "radio_button_checked"; 
     skill4.innerHTML = "radio_button_checked";
});
skill4.addEventListener('mouseout', (event) => {
     if (click == false) {
          skill1.innerHTML = "radio_button_unchecked";
          skill2.innerHTML = "radio_button_unchecked";
          skill3.innerHTML = "radio_button_unchecked";
          skill4.innerHTML = "radio_button_unchecked";
     };
});
skill4.addEventListener('click', (event) => {
     click = true;
     skill.value = 4;
     skill1.innerHTML = "radio_button_checked";
     skill2.innerHTML = "radio_button_checked";
     skill3.innerHTML = "radio_button_checked";
     skill4.innerHTML = "radio_button_checked";
});

// Taken from http://www.randomsnippets.com/2008/02/21/how-to-dynamically-add-form-elements-via-javascript/
var ingredientCounter = 1;
var ingredientLimit = 20;

function addIngredients(divName) {
     if (ingredientCounter == ingredientLimit) {
          alert("You have reached the limit of adding " + ingredientCounter + " ingredients");
     } else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Ingredient " + (ingredientCounter + 1) + " <br><input type='text' name='myIngredients[]'>";
          document.getElementById(divName).appendChild(newdiv);
          ingredientCounter++;
     }
}

var prepCounter = 1;
var prepLimit = 20;

function addPrepSteps(divName) {
     if (prepCounter == prepLimit) {
          alert("You have reached the limit of adding " + prepCounter + " preparation steps");
     } else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Preparation Step " + (prepCounter + 1) + " <br><input type='text' name='myPrepSteps[]'>";
          document.getElementById(divName).appendChild(newdiv);
          ingredientCounter++;
     }
}