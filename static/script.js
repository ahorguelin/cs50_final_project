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
        let choice = document.querySelector('#ingredient');
        let ingredient = choice.options[choice.selectedIndex].value;
        let newInput;
        let placeholder = document.querySelector('#inputs-placeholder')
        newInput = document.createElement('input');
        newInput.setAttribute('type', 'number');
        newInput.setAttribute('placeholder', ingredient);
        newInput.setAttribute('name', ingredient)
        placeholder.appendChild(newInput);
    })

    let btnRmv = document.querySelector('#rmv-ingredient');
    btnRmv.addEventListener('click', function(){
        let choice = document.querySelector('#ingredient');
        let ingredient = choice.options[choice.selectedIndex].value;
        // rmvInput = document.querySelector(`[value=${ingredient}]`)
        rmvInput = document.querySelector(`[name="${ingredient}"]`)
        rmvInput.remove()
    })

})