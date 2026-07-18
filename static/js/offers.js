document.addEventListener("DOMContentLoaded", () => {

    // ==========================
    // Animation
    // ==========================

    const cards = document.querySelectorAll(".mhs-product-card");

    const observer = new IntersectionObserver((entries) => {

        entries.forEach((entry) => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    }, {
        threshold: 0.2
    });

    cards.forEach((card) => {

        observer.observe(card);

    });


    // ==========================
    // Countdown Timer
    // ==========================

    const timers = document.querySelectorAll(".mhs-offer-timer");

    timers.forEach((timer) => {

        const startDate = new Date(
            timer.dataset.start
        ).getTime();

        const endDate = new Date(
            timer.dataset.end
        ).getTime();

        const progress = timer
            .nextElementSibling
            .querySelector(".mhs-progress-fill");


        function updateTimer() {

            const now = new Date().getTime();

            const distance = endDate - now;


            // پایان تخفیف
            if (distance <= 0) {

                timer.classList.add("mhs-offer-ended");

                timer.innerHTML = `
                    <p class="mhs-timer-title">
                        ⛔ تخفیف به پایان رسید
                    </p>
                `;

                progress.style.width = "0%";
                progress.style.background = "#ff3b30";

                return;
            }


            // درصد نوار پیشرفت
            const total = endDate - startDate;

            let percent = (distance / total) * 100;

            if (percent < 0) percent = 0;

            progress.style.width = percent + "%";


            // رنگ نوار
            if (distance < 3600000) {

                progress.style.background = "#ff3b30";

            }
            else if (distance < 86400000) {

                progress.style.background = "#ff9500";

            }
            else {

                progress.style.background = "#18c964";

            }


            // محاسبه زمان
            const days = Math.floor(
                distance / (1000 * 60 * 60 * 24)
            );

            const hours = Math.floor(
                (distance % (1000 * 60 * 60 * 24))
                / (1000 * 60 * 60)
            );

            const minutes = Math.floor(
                (distance % (1000 * 60 * 60))
                / (1000 * 60)
            );

            const seconds = Math.floor(
                (distance % (1000 * 60))
                / 1000
            );


            timer.querySelector(".days").textContent =
                String(days).padStart(2, "0");

            timer.querySelector(".hours").textContent =
                String(hours).padStart(2, "0");

            timer.querySelector(".minutes").textContent =
                String(minutes).padStart(2, "0");

            timer.querySelector(".seconds").textContent =
                String(seconds).padStart(2, "0");

        }


        updateTimer();

        setInterval(updateTimer, 1000);

    });

});