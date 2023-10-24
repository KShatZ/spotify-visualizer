const dropdownToggle = document.getElementById("dropdown-toggle");
const dropdownArrow = document.getElementById("dropdown-arrow");
const navDropdown = document.getElementById("nav-dropdown");

dropdownToggle.addEventListener("click", () => {

    if (!navDropdown.style.display || navDropdown.style.display == "none") {
        navDropdown.style.display = "block";
        dropdownArrow.classList.add("accent");
    } else {
        navDropdown.style.display = "none";
        dropdownArrow.classList.remove("accent");
    }

});