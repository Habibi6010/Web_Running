document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('uploadForm');
  const uploadSection = document.getElementById('uploadSection');
  const progressSection = document.getElementById('progressSection');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');

  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    
    // Hide the upload form and show the progress section
    uploadSection.style.display = 'none';
    progressSection.style.display = 'block';

    // Create a new FormData object and make an AJAX request
    const formData = new FormData(form);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', form.action, true);

    // Update progress bar during upload
    xhr.upload.addEventListener('progress', function(e) {
      if (e.lengthComputable) {
        const percentComplete = Math.round((e.loaded / e.total) * 100);
        progressBar.style.width = percentComplete + '%';
        progressText.textContent = percentComplete + '%';
      }
    });

    // Handle request completion
    xhr.addEventListener('load', function() {
      if (xhr.status === 200) {
        progressText.textContent = 'Upload complete!';
      } else {
        progressText.textContent = 'Upload failed. Please try again.';
      }
    });

    xhr.send(formData);
  });
});
