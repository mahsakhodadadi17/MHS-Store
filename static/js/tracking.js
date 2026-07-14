console.log("FAQ JS LOADED");

const faqs = document.querySelectorAll(".faq-item");

faqs.forEach(item => {

    const btn = item.querySelector(".faq-question");

    btn.onclick = function () {

        faqs.forEach(other => {
            if (other !== item) {
                other.classList.remove("active");
            }
        });

        item.classList.toggle("active");

    };

});