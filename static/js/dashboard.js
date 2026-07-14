const menuBtn = document.querySelector(".menu-btn");

const sidebar = document.querySelector(".sidebar");


menuBtn.addEventListener("click",()=>{


sidebar.classList.toggle("show");


});





const links = document.querySelectorAll("nav a[data-tab]");


const tabs = document.querySelectorAll(".tab");



links.forEach(link=>{


link.addEventListener("click",()=>{


let target = link.dataset.tab;



tabs.forEach(tab=>{

tab.classList.remove("active");

});



document
.getElementById(target)
.classList.add("active");



links.forEach(item=>{

item.classList.remove("active");

});



link.classList.add("active");


});

});







const removeButtons = document.querySelectorAll(".remove");


removeButtons.forEach(btn=>{


btn.onclick = ()=>{


let confirmDelete =
confirm(
"Remove this product from wishlist?"
);



if(confirmDelete){

btn.parentElement.remove();

}



}


});