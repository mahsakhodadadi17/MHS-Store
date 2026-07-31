const questions = document.querySelectorAll(".faq-question");

questions.forEach((btn) => {
  btn.addEventListener("click", () => {
    const answer = btn.nextElementSibling;

    // close other answers
    document.querySelectorAll(".faq-answer").forEach((item) => {
      if (item !== answer) item.style.display = "none";
    });

    // toggle current
    answer.style.display =
      answer.style.display === "block" ? "none" : "block";
  });
});