const registerForm = document.getElementById("registerForm");
const formError = document.getElementById("form-error");

registerForm.addEventListener("submit", async(event) => {
    
    event.preventDefault();

    const formData = new FormData(registerForm);

    const data = {
        "username": formData.get("username"),
        "password": formData.get("password")
    }

    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    const response = await fetch("/register", {
        method: "POST",
        body: JSON.stringify(data),
        headers: headers
    });

    const responseData = await response.json();
    const msg = responseData.msg;

    switch (response.status) {
        case 201:
            window.location.href = "/login";
            break;

        case 409:
            registerForm.style.height = "460px";
            formError.innerText = msg;
            formError.style.display = "block";
            break;

        case 500:
            registerForm.style.height = "460px";
            formError.innerText = msg;
            formError.style.display = "block";
            break;

        default:
            window.location.href = "/register";
            break;
    };
});