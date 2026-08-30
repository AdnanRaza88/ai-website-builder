const APP_URL = "https://your-app-name.streamlit.app";

const launchButton = document.getElementById("launch-btn");
const statusHint = document.getElementById("status-hint");

launchButton.addEventListener("click", () => {
    statusHint.textContent = "Opening the app, please wait";
    window.open(APP_URL, "_blank");
});
