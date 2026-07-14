// Simple smooth scroll effect for future navigation (optional enhancement)
document.querySelectorAll("a").forEach(link => {
  link.addEventListener("click", function(e) {
    if (this.hash !== "") {
      e.preventDefault();
      const target = document.querySelector(this.hash);
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    }
  });
});