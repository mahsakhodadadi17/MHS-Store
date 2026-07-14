document.addEventListener("DOMContentLoaded", () => {

    const totalBox = document.getElementById("lux-total-price");

    function updateTotal() {

        const cards = document.querySelectorAll(".lux-product-card");

        let total = 0;

        cards.forEach(card => {

            const price = Number(card.dataset.price);
            const qty = Number(card.querySelector(".lux-quantity").innerText);

            total += price * qty;
        });

        totalBox.innerText = "$" + total.toFixed(2);
    }

    // PLUS
    document.querySelectorAll(".lux-plus").forEach(btn => {

        btn.addEventListener("click", function () {

            const card = this.closest(".lux-product-card");
            const qty = card.querySelector(".lux-quantity");

            qty.innerText = Number(qty.innerText) + 1;

            updateTotal();
        });

    });

    // MINUS
    document.querySelectorAll(".lux-minus").forEach(btn => {

        btn.addEventListener("click", function () {

            const card = this.closest(".lux-product-card");
            const qty = card.querySelector(".lux-quantity");

            if (Number(qty.innerText) > 1) {
                qty.innerText = Number(qty.innerText) - 1;
            }

            updateTotal();
        });

    });

    // REMOVE
    document.querySelectorAll(".lux-remove").forEach(btn => {

        btn.addEventListener("click", function () {

            const card = this.closest(".lux-product-card");

            card.remove();

            updateTotal();

            if (document.querySelectorAll(".lux-product-card").length === 0) {
                totalBox.innerText = "$0.00";
            }

        });

    });

    updateTotal();
});