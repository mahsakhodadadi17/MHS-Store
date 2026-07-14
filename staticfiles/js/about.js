document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll(".contact-card");

    cards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.style.transition = "all 0.4s ease";
        });
    });

});