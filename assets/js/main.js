/**
* Template Name: MyResume
* Template URL: https://bootstrapmade.com/free-html-bootstrap-template-my-resume/
* Updated: Jun 29 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Header toggle
   */
  const headerToggleBtn = document.querySelector('.header-toggle');

  function headerToggle() {
    document.querySelector('#header').classList.toggle('header-show');
    headerToggleBtn.classList.toggle('bi-list');
    headerToggleBtn.classList.toggle('bi-x');
  }
  headerToggleBtn.addEventListener('click', headerToggle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll('#navmenu a').forEach(navmenu => {
    navmenu.addEventListener('click', () => {
      if (document.querySelector('.header-show')) {
        headerToggle();
      }
    });

  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      this.parentNode.classList.toggle('active');
      this.parentNode.nextElementSibling.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector('.scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }
  scrollTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  window.addEventListener('load', toggleScrollTop);
  document.addEventListener('scroll', toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }
  window.addEventListener('load', aosInit);

  /**
   * Init typed.js
   */
  const selectTyped = document.querySelector('.typed');
  if (selectTyped) {
    let typed_strings = selectTyped.getAttribute('data-typed-items');
    typed_strings = typed_strings.split(',');
    new Typed('.typed', {
      strings: typed_strings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000
    });
  }

  /**
   * Initiate Pure Counter
   */
  new PureCounter();

  /**
   * Animate the skills items on reveal
   */
  let skillsAnimation = document.querySelectorAll('.skills-animation');
  skillsAnimation.forEach((item) => {
    new Waypoint({
      element: item,
      offset: '80%',
      handler: function(direction) {
        let progress = item.querySelectorAll('.progress .progress-bar');
        progress.forEach(el => {
          el.style.width = el.getAttribute('aria-valuenow') + '%';
        });
      }
    });
  });

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: '.glightbox'
  });

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll('.isotope-layout').forEach(function(isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
    imagesLoaded(isotopeItem.querySelector('.isotope-container'), function() {
      initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });
    });

    isotopeItem.querySelectorAll('.isotope-filters li').forEach(function(filters) {
      filters.addEventListener('click', function() {
        isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
        this.classList.add('filter-active');
        initIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        if (typeof aosInit === 'function') {
          aosInit();
        }
      }, false);
    });

  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Correct scrolling position upon page load for URLs containing hash links.
   */
  window.addEventListener('load', function(e) {
    if (window.location.hash) {
      if (document.querySelector(window.location.hash)) {
        setTimeout(() => {
          let section = document.querySelector(window.location.hash);
          let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
          window.scrollTo({
            top: section.offsetTop - parseInt(scrollMarginTop),
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });

  /**
   * Navmenu Scrollspy
   */
  let navmenulinks = document.querySelectorAll('.navmenu a');

  function navmenuScrollspy() {
    navmenulinks.forEach(navmenulink => {
      if (!navmenulink.hash) return;
      let section = document.querySelector(navmenulink.hash);
      if (!section) return;
      let position = window.scrollY + 200;
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        document.querySelectorAll('.navmenu a.active').forEach(link => link.classList.remove('active'));
        navmenulink.classList.add('active');
      } else {
        navmenulink.classList.remove('active');
      }
    })
  }
  window.addEventListener('load', navmenuScrollspy);
  document.addEventListener('scroll', navmenuScrollspy);


  document.addEventListener('DOMContentLoaded', function() {
    const profileButton = document.querySelector('.profile-button');
    const dropdownMenu = document.querySelector('.dropdown-menu');
  
    profileButton.addEventListener('click', function() {
      const isExpanded = profileButton.getAttribute('aria-expanded') === 'true';
      profileButton.setAttribute('aria-expanded', !isExpanded);
      dropdownMenu.style.display = isExpanded ? 'none' : 'block';
    });
  
    // Close the dropdown if the user clicks outside of it
    document.addEventListener('click', function(event) {
      if (!profileButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
        profileButton.setAttribute('aria-expanded', 'false');
        dropdownMenu.style.display = 'none';
      }
    });
  });
  


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
  





})();

// submit signin form
function handelSigninButton(event) {
  event.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const data = {
    email,
    password
  }
  /*
  fetch('https://reqres.in/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }).then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
      } else {
        alert('Login successful');
      }
    });*/
    if (email == "" || password == "") 
    {
      alert("Please Enter Email or Password");
      return false;
    }

    // Regular expression for validating an email address
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      alert("Please enter a valid email address.");
      return false;
    }

    alert('Login successful: \n' + email + ' \n' + password);
}

// foget password button 
function forgotPassword() {
  // Prompt the user to enter their email address
  var email = prompt("Please enter your email address to reset your password:");
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (email != "") {
      if (!emailRegex.test(email)) {
          alert("Please enter a valid email address.");
          return;
      }
      // Here you can add an AJAX request to send the email to the server
      // For now, we'll just simulate a password reset request
      alert("A password reset link has been sent to " + email);
  } else {
      alert("Email address is required to reset your password.");
  }
}

// sumbit contact us form

function handelContactUsButton(event) {

  event.preventDefault(); // Prevent form from submitting the default way
            
  // Get form elements
  const name = document.getElementById('contact-name').value.trim();
  const email = document.getElementById('contact-email').value.trim();
  const subject = document.getElementById('contact-subject').value.trim();
  const message = document.getElementById('contact-message').value.trim();
 // const errorMessageElement = document.getElementById('error-message');
  
  // Regular expression for validating an email address
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  // Validation checks
  if (name =="" || email =="" || subject =="" || message == "") {
    alert("All contact fields are required.");
    return;
  }
  
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address for contact.");
    return;
  }
  
  // If validation passes, process the form data
  alert(`Name: ${name}\nEmail: ${email}\nSubject: ${subject}\nMessage: ${message}`);
  //reset form
  document.getElementById('contact-form').reset();
  // Show success message
  alert('Thank you for contacting us');
}

// Show video preview when a file is selected for upload 
function previewVideo() {
  const fileInput = document.getElementById('videoUpload');
  const videoPreview = document.getElementById('videoPreview');
  const file = fileInput.files[0];
  
  if (file) {
      const fileURL = URL.createObjectURL(file);
      videoPreview.src = fileURL;
      videoPreview.style.display = 'block';
  } else {
      videoPreview.style.display = 'none';
  }
}

// get rgb color from hex color
function hexToRgb(hex) {
  hex = hex.replace(/^#/, '');

  let bigint = parseInt(hex, 16);
  let r = (bigint >> 16) & 255;
  let g = (bigint >> 8) & 255;
  let b = bigint & 255;

  return `rgb(${r}, ${g}, ${b})`;
}

// get hex color from selected color button
function getColorRGB(settingNumber) {
  const colorInput = document.getElementById(`colorSetting${settingNumber}`);
  const hexColor = colorInput.value;
  const rgbColor = hexToRgb(hexColor);
  console.log(`Setting ${settingNumber} Color (RGB):`, rgbColor);
  alert(`Setting ${settingNumber} Color (RGB): ${rgbColor}`);
}

// Function to clear all settings (uncheck all checkboxes)
function clearSettings() {
  const settings = document.querySelectorAll('input[type="checkbox"]');
  settings.forEach(setting => {
      setting.checked = false;
  });
}

// Function to automatically select settings based on the button clicked
function selectSettings(settingNumbers) {
  const settings = document.querySelectorAll('input[type="checkbox"]');
  settings.forEach(setting => {
      setting.checked = false; // Uncheck all settings first
  });
  settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true; // Check specific settings
  });
}