const loginForm = document.getElementById("loginForm");
const formError = document.getElementById("form-error");

loginForm.addEventListener("submit", async(event) => {
    
    event.preventDefault();

    const formData = new FormData(loginForm);

    const data = {
        "username": formData.get("username"),
        "password": formData.get("password")
    }

    const headers = new Headers();
    headers.append("Content-Type", "application/json");

    const response = await fetch("/login", {
        method: "POST",
        body: JSON.stringify(data),
        headers: headers
    });

    const responseData = await response.json();
    const msg = responseData.msg;

    switch (response.status) {
        case 200:
            window.location.href = "/";
            break;

        case 400:
            loginForm.style.height = "460px";
            formError.innerText = msg;
            formError.style.display = "block";
            break;

        case 401:
            window.location.href = "/spotify/auth";
            break;  

        case 500:
            loginForm.style.height = "460px";
            formError.innerText = msg;
            formError.style.display = "block";
            break;

        default:
            window.location.href = "/login";
            break;
    };
});