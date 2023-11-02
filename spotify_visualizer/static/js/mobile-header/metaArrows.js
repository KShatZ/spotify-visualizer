const arrowOffClass = "meta-arrow-off";

const rightArrow = document.getElementById("meta-arrow-right");
const leftArrow = document.getElementById("meta-arrow-left");

const headerMeta = document.getElementById("header-meta");
const metaImage = document.getElementById("meta-image");


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

    if (leftArrow.classList.contains(arrowOffClass)) {
        return;
    }

    if (rightArrow.classList.contains(arrowOffClass)) {
        rightArrow.classList.remove(arrowOffClass);
    }


    leftArrow.classList.add(arrowOffClass);

    metaImage.style.display = "flex";
    headerMeta.style.display = "none";
    
});

// ------ Swipe Functionality ------ //
let initialX = null;

const handleSwipe = (change) => {
    if (change > 4) { // Right Swipe

        if (rightArrow.classList.contains(arrowOffClass)) {
            return;
        }
    
        rightArrow.classList.add(arrowOffClass);

        if (leftArrow.classList.contains(arrowOffClass)) {
            leftArrow.classList.remove(arrowOffClass);
        }
    
        metaImage.style.display = "none";
        headerMeta.style.display = "flex";

    } else if (change < -4) { // Left Swipe

        if (leftArrow.classList.contains(arrowOffClass)) {
            return;
        }

        leftArrow.classList.add(arrowOffClass);

        if (rightArrow.classList.contains(arrowOffClass)) {
            rightArrow.classList.remove(arrowOffClass);
        }
    
        metaImage.style.display = "flex";
        headerMeta.style.display = "none";
    }
}

metaImage.addEventListener("touchstart", (e) => {
    initialX = e.touches[0].clientX;
});

headerMeta.addEventListener("touchstart", (e) => {
    initialX = e.touches[0].clientX;
});

headerMeta.addEventListener("touchmove", (e) => {
    if (initialX === null) {
        return;
    }

    let currentX = e.touches[0].clientX;
    const changeInX = currentX - initialX;

    handleSwipe(changeInX);
    initialX = null;
});

metaImage.addEventListener("touchmove", (e) => {
    if (initialX === null) {
        
        return;
    }

    let currentX = e.touches[0].clientX;
    const changeInX = currentX - initialX;
    
    handleSwipe(changeInX);
    initialX = null;
});
