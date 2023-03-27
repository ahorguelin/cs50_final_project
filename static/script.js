document.addEventListener('DOMContentLoaded', function(){
    let nav = document.querySelector('.navbar');
    let hamburger = document.querySelector('#hamburger');
    let iconTop = document.querySelector('.icon-bar');
    let iconMid = document.querySelector('.middle');
    let iconBot = document.querySelector('.bottom');
    hamburger.addEventListener('click', function(){
        if (nav.classList.contains("show-menu")){
            nav.classList.remove("show-menu");
            iconTop.classList.remove('animated');
            iconMid.classList.remove('animated');
            iconBot.classList.remove('animated');
        }
        else{
            nav.classList.add("show-menu");
            iconTop.classList.add('animated');
            iconMid.classList.add('animated');
            iconBot.classList.add('animated');
        }
    })

    if (document.querySelector('#add-ingredient')){
        let btnAdd = document.querySelector('#add-ingredient');
        btnAdd.addEventListener('click', function(){
            //select the multiple choices
            let choice = document.querySelector('#ingredient');
    
            //select the chosen ingredient
            let ingredient_id = choice.options[choice.selectedIndex].value;
            let ingredient_name = choice.options[choice.selectedIndex].text;
            let newInput;
            let placeholder = document.querySelector('#inputs-placeholder');
    
            //create parent div for label input & button
            newDiv = document.createElement('div');
            newDiv.setAttribute('id', `div-ingredient-${ingredient_id}`);
            newDiv.setAttribute('class', 'input');
    
            //create div that will contain input & btn together
            dataDiv = document.createElement('div');
    
            //create the label
            newLabel = document.createElement('label');
            newLabel.innerHTML = ingredient_name;
            newLabel.setAttribute('for', ingredient_name);
           
            //create the input based on this info. Append it in the placeholder div
            newInput = document.createElement('input');
            newInput.setAttribute('class', 'dynamic-input');
            newInput.setAttribute('id', ingredient_name);
            newInput.setAttribute('type', 'number');
            newInput.setAttribute('step', '0.1');
            newInput.setAttribute('min', '0');
            newInput.setAttribute('placeholder', 'Gramms');
            newInput.setAttribute('name', ingredient_id);
            
            //create a button with necessary info next to it
            newBtn = document.createElement('button');
            newBtn.setAttribute('class', 'rmv-ingredient');
            newBtn.setAttribute('type', 'button');
            newBtn.setAttribute('name', ingredient_name);
            newBtn.setAttribute('data-ingredient-id', ingredient_id);
            newBtn.innerHTML = "X";
    
            //add input, label and btn
            dataDiv.appendChild(newInput);
            dataDiv.appendChild(newBtn);
            newDiv.appendChild(newLabel);
            newDiv.appendChild(dataDiv);
            placeholder.appendChild(newDiv);
    
            //remove the chosen input from the list
            document.querySelector(`[value="${ingredient_id}"]`).remove();
            //add deleted choice to removable ingredients
        })
    }

    //Targeting body allows us to add event listener to elements created dynamically
    document.querySelector('body').addEventListener('click', function(event) {
        if (event.target.classList == 'rmv-ingredient'){
            //get the btn info
            let ingredientId = event.target.dataset['ingredientId'];
            let ingredientName = event.target.name;

            //remove div 
            rmvInput = document.querySelector(`#div-ingredient-${ingredientId}`);
            rmvInput.remove();

            //add option back
            newOption = document.createElement('option');
            newOption.setAttribute('value', ingredientId);
            newOption.innerHTML = ingredientName;

            //add the deleted option back to possibilites
            let deletedChoice = document.querySelector('#ingredient');
            deletedChoice.appendChild(newOption);
        }
    })

    if (document.querySelector('.collapsible')){
        let btn = document.querySelector('.collapsible');
        btn.addEventListener('click', function() {
            let div = document.querySelector('.collapsible-div');
            if (div.style.maxHeight){
                div.style.maxHeight = null;
            }
            else{
                div.style.maxHeight = div.scrollHeight +"px";
            }
        })
    }
})