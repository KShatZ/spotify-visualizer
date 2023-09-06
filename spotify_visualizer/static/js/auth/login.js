const loginForm = document.getElementById("loginForm");

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

    switch (response.status) {
        case 200:
            window.location.href = "/blocked";
            break;
        case 401:
            window.location.href = "/spotify/auth";
            break;    
        default:
            window.location.href = "/login";
            break;
    };
});