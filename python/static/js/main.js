/**
* Template Name: MyResume
* Template URL: https://bootstrapmade.com/free-html-bootstrap-template-my-resume/
* Updated: Jun 29 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function () {
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
    navmenu.addEventListener('click', function (e) {
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
      handler: function (direction) {
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
  document.querySelectorAll('.isotope-layout').forEach(function (isotopeItem) {
    let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
    let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
    let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

    let initIsotope;
    imagesLoaded(isotopeItem.querySelector('.isotope-container'), function () {
      initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
        itemSelector: '.isotope-item',
        layoutMode: layout,
        filter: filter,
        sortBy: sort
      });
    });

    isotopeItem.querySelectorAll('.isotope-filters li').forEach(function (filters) {
      filters.addEventListener('click', function () {
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
    document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
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
  window.addEventListener('load', function (e) {
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


  document.addEventListener('DOMContentLoaded', function () {
    const profileButton = document.querySelector('.profile-button');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    profileButton.addEventListener('click', function () {
      const isExpanded = profileButton.getAttribute('aria-expanded') === 'true';
      profileButton.setAttribute('aria-expanded', !isExpanded);
      dropdownMenu.style.display = isExpanded ? 'none' : 'block';
    });

    // Close the dropdown if the user clicks outside of it
    document.addEventListener('click', function (event) {
      if (!profileButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
        profileButton.setAttribute('aria-expanded', 'false');
        dropdownMenu.style.display = 'none';
      }
    });
  });

})();

// add listener to user-details page to get user details when page load
document.addEventListener('DOMContentLoaded', function () {
  // extract username from url
  const urlParams = new URLSearchParams(window.location.search);
  const username = urlParams.get('username') || 'Profile';
  // Update span for show username
  document.getElementById("usernameDisplay").innerText = username;
});

// submit signin form
function handelSigninButton(event) {
  event.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  if (email == "" || password == "") {
    alert("Please Enter Email or Password");
    return false;
  }
  // Regular expression for validating an email address
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address.");
    return false;
  }
  const data = {
    email,
    password
  }
  fetch('http://18.116.29.76:5001/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      if (data.accsess) {
        alert('Login successful: \n' + email);
        window.location.href = `http://18.116.29.76:5001/dashboard?username=${encodeURIComponent(email)}`;
      }
      else {
        alert('Login failed: \n' + 'Invalid email or password');
      }
    })
    .catch(error => {
      alert("Server Error"+error.message);
    });
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
  if (name == "" || email == "" || subject == "" || message == "") {
    alert("All contact fields are required.");
    return;
  }

  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address for contact.");
    return;
  }
  // If validation passes, process the form data
  const data = {
    name,
    email,
    subject,
    message
  }
  fetch('http://18.116.29.76:5001/contact_us', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      if (data.accsess) {
        alert('Thank you for contacting us');
      }
      else {
        alert('Sending failed \n' + 'Please try again later');
      }
    })
    .catch(error => {
      alert("Server Error");
    });

  //reset form
  document.getElementById('contact-form').reset();
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
  return [r, g, b];
}

let toe_off = true;
let full_flight = true;
let touch_down = true;
let full_support = true;
let clear = true;

function toe_off_click(settingNumbers) {
  const button = document.getElementById('toe_off');
  if (toe_off) {
    toe_off = false;
    button.style.backgroundColor = 'green';
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true; // Check specific settings
    });
  } else {
    toe_off = true;
    button.style.backgroundColor = '#007BFF';
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = false; // Check specific settings
    });
    clear = true;
    document.getElementById('clear').style.backgroundColor = '#007BFF';
    document.getElementById("clear").innerText = "Select All";
  }
  select_button_check();
  select_checkbox();
  check_radio();

}
function full_flight_click(settingNumbers) {
  const button = document.getElementById('full_flight');
  if (full_flight) {
    full_flight = false;
    button.style.backgroundColor = 'green';
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true; // Check specific settings
    });
  } else {
    full_flight = true;
    button.style.backgroundColor = '#007BFF';
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = false; // Check specific settings
    });
    clear = true;
    document.getElementById('clear').style.backgroundColor = '#007BFF';
    document.getElementById("clear").innerText = "Select All";
  }
  select_button_check();
  select_checkbox();
  check_radio();
}
function touch_down_click(settingNumbers) {
  const button = document.getElementById('touch_down');
  if (touch_down) {
    touch_down = false;
    button.style.backgroundColor = 'green';
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true; // Check specific settings
    });
  } else {
    touch_down = true;
    button.style.backgroundColor = '#007BFF';
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = false; // Check specific settings
    });
    clear = true;
    document.getElementById('clear').style.backgroundColor = '#007BFF';
    document.getElementById("clear").innerText = "Select All";
  }
  select_button_check();
  select_checkbox();
  check_radio();
}

function full_support_click(settingNumbers) {
  const button = document.getElementById('full_support');
  if (full_support) {
    full_support = false;
    button.style.backgroundColor = 'green';
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true; // Check specific settings
    });
  } else {
    full_support = true;
    button.style.backgroundColor = '#007BFF';
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = false; // Check specific settings
    });
    clear = true;
    document.getElementById('clear').style.backgroundColor = '#007BFF';
    document.getElementById("clear").innerText = "Select All";
  }
  select_button_check();
  select_checkbox();
  check_radio();
}
function clear_click() {
  
  const button = document.getElementById('clear');
  const settings = document.querySelectorAll('input[type="checkbox"]');
  if (clear) {
    clear = false;
    button.style.backgroundColor = 'green';
    settings.forEach(setting => {
      setting.checked = true;
    });
    document.getElementById("clear").innerText = "Clear All";
    full_support = false;
    document.getElementById('full_support').style.backgroundColor = 'green';
    full_flight = false;
    document.getElementById('full_flight').style.backgroundColor = 'green';
    touch_down = false;
    document.getElementById('touch_down').style.backgroundColor = 'green';
    toe_off = false;
    document.getElementById('toe_off').style.backgroundColor = 'green';
  } else {
    clear = true;
    button.style.backgroundColor = '#007BFF';
    settings.forEach(setting => {
      setting.checked = false;
    });
    document.getElementById("clear").innerText = "Select All";
    full_support = true;
    document.getElementById('full_support').style.backgroundColor = '#007BFF';
    full_flight = true;
    document.getElementById('full_flight').style.backgroundColor = '#007BFF';
    touch_down = true;
    document.getElementById('touch_down').style.backgroundColor = '#007BFF';
    toe_off = true;
    document.getElementById('toe_off').style.backgroundColor = '#007BFF';
  }
  check_radio();
}

function select_button_check() {
  if (!(toe_off || full_flight || touch_down || full_support)) {
    document.getElementById('clear').style.backgroundColor = 'green';
    document.getElementById("clear").innerText = "Clear All";
    clear = false;
  }
}
function select_checkbox() {
  const settingNumbers = [];
  if (!toe_off) {
    settingNumbers.push(...[1, 2, 3, 4, 5, 6, 7, 8, 9]);
  }
  if (!full_flight) {
    settingNumbers.push(...[2, 3, 6, 10, 11]);
  }
  if (!touch_down) {
    settingNumbers.push(...[5, 6, 8, 12, 13, 14]);
  }
  if (!full_support) {
    settingNumbers.push(...[2, 6, 9, 13]);
  }
  settingNumbers.forEach(number => {
    document.getElementById(`setting${number}`).checked = true; // Check specific settings
  });
}

// Send and receive data from server and work with API
function sendData(event) {

  event.preventDefault(); // Stop form from submitting the traditional way
  check_radio();
  if (document.getElementById('videoUpload').files.length == 0) {
    alert("You didn't upload video.");
    return;
  }
  const loading = document.getElementById('parent-container');
  const loading2 = document.getElementById('loading');

  // Show the loading GIF
  loading.style.display = 'block';
  loading2.style.display = 'block';

  // Get the form element
  const form = document.getElementById('uploadForm');
  // Create a new FormData object
  const formData = new FormData(form);
  // Get height_runner from the input field
  const height_runner = document.getElementById('numberInput').value;
  // Get selected AI model (radio buttons)
  const selectedModel = document.querySelector('input[name="model"]:checked').value;
  // Get usrname from usernameeDisplay span
  const username = document.getElementById('usernameDisplay').innerText;

  // Get active section
  const active_section = document.getElementById('result');
  //Get result video preview
  const resultVideoPreview = document.getElementById('resultVideoPreview');
  // Manually add the selected checkboxes and colors to the formData
  const settings_colors = {};

  for (let i = 1; i <= 14; i++) {
    const checkbox = document.getElementById(`setting${i}`);
    const colorInput = document.getElementById(`colorSetting${i}`);
    settings_colors[document.getElementById(`setting${i}`).value] = [checkbox.checked, hexToRgb(colorInput.value)];
  }
  //Append the height_runner, selectedModel, and settings_colors to the formData
  formData.append('height_runner', height_runner);
  formData.append('selectedModel', selectedModel);
  formData.append('settings_colors', JSON.stringify(settings_colors));
  formData.append('username', username);
  
  // Send the data to the server
  fetch('http://18.116.29.76:5001/run_analysis', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.response) {
        // alert('Data sent successfully and Model is running');
        // Hide the loading GIF
        loading.style.display = 'none';
        loading2.style.display = 'none';
        //Show reslut video
        active_section.style.display = 'block';
        resultVideoPreview.style.display = 'block';
        console.log(data.link);
        resultVideoPreview.src = data.link;
        resultVideoPreview.load();
        resultVideoPreview.play();

        // Download result video link
        downloadLink = document.getElementById('downloadResultVideo');
        downloadLink.href = "download_video/"+data.videoaddress;
        //downloadLink.download = data.link.split('/').pop(); //Extract file name from path
        downloadLink.style.display = 'inline-block'; // Show the download link

        // Download the CSV file link
        downloadLink = document.getElementById('downloadResultCSV');
        downloadLink.href = "download_csv/"+data.csvaddress;
        // downloadLink.download = data.csvaddress.split('/').pop(); //Extract file name from path
        downloadLink.style.display = 'inline-block'; // Show the download link

      } else {
        alert('Data sent failed');
        // Hide the loading GIF
        loading.style.display = 'none';
        loading2.style.display = 'none';
        active_section.style.display = 'none';
        resultVideoPreview.style.display = 'none';
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert("Data sent failed".error.message);
      // Hide the loading GIF
      loading.style.display = 'none';
      loading2.style.display = 'none';
      active_section.style.display = 'none';
      resultVideoPreview.style.display = 'none';
    });
}

function check_yolo(checkbox, text) {
  let radios = document.getElementsByName('model');
  let modelType = "";
  for (let i = 0; i < radios.length; i++) {
    if (radios[i].checked) {
      modelType = radios[i].value;
      break;
    }
  }
  if (checkbox.checked && modelType == "yolo") {
    alert("AI model you select can't analysis " + text)
    checkbox.checked = false
  }
}

function check_radio() {
  if (document.querySelector('input[name="model"]:checked').value == 'yolo') {
    let set1 = document.getElementById("setting1");
    let set2 = document.getElementById("setting2");
    let set3 = document.getElementById("setting6");
    let set4 = document.getElementById("setting13");
    if (set1.checked || set2.checked || set3.checked || set4.checked) {
      set1.checked = false;
      set2.checked = false;
      set3.checked = false;
      set4.checked = false;
      alert(" You selected analysis setting are not compatible with AI model you selected");
    }
  }
}

// add listener to view profile click and send username to profile page
document.getElementById("videprofileLink").addEventListener("click", function (event) {
  event.preventDefault();
  const username = document.getElementById('usernameDisplay').innerText;
  window.location.href = `profile.html?username=${encodeURIComponent(username)}`;
});

// add listener to profile page to get user details when page load
document.addEventListener('DOMContentLoaded', function () {
  // extract username from url
  const urlParams = new URLSearchParams(window.location.search);
  const username = urlParams.get('username') || 'No-Profile';
  // Update span for show username
  document.getElementById("usernameDisplay").innerText = username;
});
