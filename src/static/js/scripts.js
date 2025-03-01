document.addEventListener("DOMContentLoaded", function () {
  // Update file label with the selected file name
  const fileInput = document.getElementById("video-input");
  const fileLabel = document.getElementById("file-label");
  if (fileInput && fileLabel) {
    fileInput.addEventListener("change", function () {
      if (fileInput.files.length > 0) {
        fileLabel.textContent = fileInput.files[0].name;
      }
    });
  }

  // Show loading indicator on form submission
  const form = document.querySelector('.upload-form');
  if (form) {
    form.addEventListener('submit', function () {
      const loadingIndicator = document.getElementById('loading-indicator');
      if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
      }
    });
  }
});
