document.addEventListener("DOMContentLoaded", function () {
  const owl = document.getElementById("owlMascot");
  const form = document.getElementById("signupForm");

  const inputs = form.querySelectorAll("input");

  inputs.forEach(input => {
    input.addEventListener("focus", () => {
      owl.style.transform = "scale(1.1)";
    });
    input.addEventListener("blur", () => {
      owl.style.transform = "scale(1)";
    });
  });

  form.addEventListener("submit", () => {
    owl.style.transform = "rotate(360deg)";
  });
});

