
document.addEventListener(
"DOMContentLoaded",
()=>{


const cards =
document.querySelectorAll(
".mhs-product-card"
);



const observer =
new IntersectionObserver(
(entries)=>{


entries.forEach(
(entry)=>{


if(entry.isIntersecting){

entry.target.classList.add(
"show"
);


}

});


},
{

threshold:.2

}

);




cards.forEach(
(card)=>{

observer.observe(card);

});



});
