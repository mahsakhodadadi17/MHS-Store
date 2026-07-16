console.log("cart.js loaded");
console.log("cart.js loaded");


function getCookie(name) {
    let cookieValue = null;

    document.cookie.split(";").forEach(c => {
        c = c.trim();

        if (c.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(
                c.substring(name.length + 1)
            );
        }
    });

    return cookieValue;
}


document.addEventListener("click", function (e) {


    /* =====================
       ADD TO CART
    ===================== */

    const addBtn = e.target.closest(".add-to-cart");

    if (addBtn) {

        e.preventDefault();


        fetch(`/add-to-cart/${addBtn.dataset.id}/`, {

            method: "POST",

            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest"
            }

        })

        .then(res => res.json())

        .then(data => {

            if (data.added) {
                window.location.href = "/cart/";
            }

        });


        return;
    }



    /* =====================
       REMOVE FROM CART
    ===================== */

    const removeBtn = e.target.closest(".lux-remove");

    if (removeBtn) {


        fetch(`/cart/remove/${removeBtn.dataset.id}/`, {

            method: "POST",

            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest"
            }

        })

        .then(res => res.json())

        .then(data => {

            if (data.success) {

                removeBtn
                .closest(".lux-product-card")
                .remove();

            }

        });


        return;
    }




    /* =====================
       PLUS / MINUS CART
    ===================== */


    const plusBtn = e.target.closest(".lux-plus");

    const minusBtn = e.target.closest(".lux-minus");


    if (plusBtn || minusBtn) {


        const btn = plusBtn || minusBtn;


        const productId = btn.dataset.id;


        const action = plusBtn ? "plus" : "minus";



        fetch(`/cart/update/${productId}/`, {


            method: "POST",


            headers: {

                "X-CSRFToken": getCookie("csrftoken"),

                "X-Requested-With": "XMLHttpRequest",

                "Content-Type": "application/x-www-form-urlencoded"

            },


            body: `action=${action}`


        })


        .then(res => res.json())


        .then(data => {


            console.log(data);



            if (data.status === "ok") {

                location.reload();

            }


        });



        return;

    }



});