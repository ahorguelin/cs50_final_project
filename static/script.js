document.addEventListener('DOMContentLoaded', function(){
    let nav = document.querySelector('.navbar');
    let hamburger = document.querySelector('#hamburger');
    hamburger.addEventListener('click', function(){
        if (nav.classList.contains("show-menu")){
            nav.classList.remove("show-menu");
        }
        else{
            nav.classList.add("show-menu");
        }
    })
    let btnAdd = document.querySelector('#add-ingredient');
    btnAdd.addEventListener('click', function(){
        //select the multiple choices
        let choice = document.querySelector('#ingredient');

        //select the chosen ingredient
        let ingredient_id = choice.options[choice.selectedIndex].value;
        let ingredient_name = choice.options[choice.selectedIndex].text;
        let newInput;
        let placeholder = document.querySelector('#inputs-placeholder')

        //create parent div
        newDiv = document.createElement('div');
        newDiv.setAttribute('id', `div-ingredient-${ingredient_id}`)
        newDiv.setAttribute('class', 'input')

        //create the label
        newLabel = document.createElement('label');
        newLabel.innerHTML = ingredient_name;
        newLabel.setAttribute('for', ingredient_name);
       
        //create the input based on this info. Append it in the placeholder div
        newInput = document.createElement('input');
        newInput.setAttribute('class', 'dynamic-input');
        newInput.setAttribute('id', ingredient_name);
        newInput.setAttribute('type', 'number');
        newInput.setAttribute('placeholder', 'Weight in gramms');
        newInput.setAttribute('name', ingredient_id);
        
        //add input and label
        newDiv.appendChild(newLabel);
        newDiv.appendChild(newInput);
        placeholder.appendChild(newDiv);

        //remove the chosen input from the list
        document.querySelector(`[value="${ingredient_id}"]`).remove()
        //add deleted choice to removable ingredients
        let addedChoice = document.querySelector('#added-ingredient');
        newOption = document.createElement('option');
        newOption.setAttribute('value', ingredient_id)
        newOption.innerHTML = ingredient_name
        addedChoice.appendChild(newOption)
    })

    let btnRmv = document.querySelector('#rmv-ingredient');
    btnRmv.addEventListener('click', function(){
        //get the necessary info
        let choice = document.querySelector('#added-ingredient');
        let ingredient_id = choice.options[choice.selectedIndex].value;
        let ingredient_name = choice.options[choice.selectedIndex].text;

        //grab the div to be deleted based on user input
        rmvInput = document.querySelector(`#div-ingredient-${ingredient_id}`);
        rmvInput.remove();
        
        //remove the choice from the option 
        document.querySelector(`[value="${ingredient_id}"]`).remove()

        //create the deleted option to be added back on usable ingredients
        newOption = document.createElement('option');
        newOption.setAttribute('value', ingredient_id)
        newOption.innerHTML = ingredient_name

        //add the deleted option back to possibilites
        let deletedChoice = document.querySelector('#ingredient');
        deletedChoice.appendChild(newOption)

    })

})