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
})