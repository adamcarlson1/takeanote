/* static/js/scripts.js */

document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("video-input");
    const fileLabel = document.getElementById("file-label");

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            if (fileInput.files.length > 0) {
                fileLabel.textContent = fileInput.files[0].name;
            }
        });
    }
});