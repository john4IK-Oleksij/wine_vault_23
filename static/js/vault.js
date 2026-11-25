document.addEventListener("DOMContentLoaded", function () {
  var toggleBtn = document.getElementById("vault-burger-toggle");
  var navMenu = document.getElementById("vault-nav-menu");

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener("click", function () {
      var isExpanded = toggleBtn.getAttribute("aria-expanded") === "true";
      toggleBtn.setAttribute("aria-expanded", !isExpanded);
      toggleBtn.classList.toggle("vault-burger-btn--active");
      navMenu.classList.toggle("vault-navigation--open");
    });
  }
});
