const updateButton = document.getElementById("update-playlist-btn");
const playlistID = updateButton.getAttribute("value");

const fetch_url = `/playlist/update/${playlistID}`;
const fetch_options = {
    "method": "POST",
    "headers": {
        "Content-Type": "application/json",
    },
};

updateButton.addEventListener("click", async () => {

    const response = await fetch(fetch_url, fetch_options);
    
    if (response.status == 200) {
        const data = await response.json();

        window.location.href = `/playlist/${data["playlist"]["id"]}?update=spotify`;
    }

    // TODO: Handle 500 
});
