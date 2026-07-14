const form = document.getElementById("register-form");


form.addEventListener("submit", function(e){


const password1 =
document.querySelector(
"input[name='password1']"
).value;



const password2 =
document.querySelector(
"input[name='password2']"
).value;




if(password1 !== password2){


e.preventDefault();


alert(
"رمز عبور و تکرار آن یکی نیست"
);


}



});