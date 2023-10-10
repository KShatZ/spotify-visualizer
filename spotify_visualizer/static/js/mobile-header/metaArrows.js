const arrowOffClass = "meta-arrow-off";

const rightArrow = document.getElementById("meta-arrow-right");
const leftArrow = document.getElementById("meta-arrow-left");

const headerMeta = document.getElementById("header-meta");
const metaImage = document.getElementById("meta-image")


rightArrow.addEventListener("click", () => {

    if (rightArrow.classList.contains(arrowOffClass)) {
        return;
    }
    
    if (leftArrow.classList.contains(arrowOffClass)) {
        leftArrow.classList.remove(arrowOffClass);
    }

    rightArrow.classList.add(arrowOffClass);

    metaImage.style.display = "none";
    headerMeta.style.display = "flex";
    
});


leftArrow.addEventListener("click", () => {

    if (rightArrow.classList.contains(arrowOffClass)) {
        rightArrow.classList.remove(arrowOffClass);
    }

    if (leftArrow.classList.contains(arrowOffClass)) {
        return;
    }

    leftArrow.classList.add(arrowOffClass);

    metaImage.style.display = "flex";
    headerMeta.style.display = "none";
    
});
