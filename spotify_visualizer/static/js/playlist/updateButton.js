const path = window.location.pathname;
const playlistId = path.slice(10);

const fetch_url = `/playlist/update/${playlistId}`;
const fetch_options = {
    "method": "POST",
    "headers": {
        "Content-Type": "application/json"
    }
};

const updateButton = document.getElementById("update-playlist-btn");
updateButton.addEventListener("click", async () => {

    const response = await fetch(fetch_url, fetch_options);
    
    if (response.status == 200) {
        const data = await response.json();

        window.location.href = `/playlist/${data["playlist"]["id"]}`;
    }

    // TODO: Handle 500 

});
