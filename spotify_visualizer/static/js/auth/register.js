const registerForm = document.getElementById("registerForm");

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

    switch (response.status) {
        case 201:
            console.log("Inside 201")
            window.location.href = "/login";
            break;    
        default:
            window.location.href = "/register";
            break;
    };
});