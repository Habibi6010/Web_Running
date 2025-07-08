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
  // Only add event listener if headerToggleBtn exists
  if (headerToggleBtn) {
    headerToggleBtn.addEventListener('click', headerToggle);
  }

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
  // Set the link to dashboard links
  const dashboardLink1 = document.getElementById("doshboardlink1");
  if (dashboardLink1) {
    dashboardLink1.href = `http://${fetch_address}:5001/dashboard?username=${encodeURIComponent(username)}`;
  }
  const dashboardLink2 = document.getElementById("dashboardlink2");
  if (dashboardLink2) {
    dashboardLink2.href = `http://${fetch_address}:5001/dashboard?username=${encodeURIComponent(username)}`;
  }
  FillHistoryTable(username);
});

// fetch_address = "13.59.211.224"
fetch_address = "127.0.0.1"
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
  
  fetch('http://'+fetch_address+':5001/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      if (data.accsess) {
        window.location.href = `http://${fetch_address}:5001/dashboard?username=${encodeURIComponent(email)}`;
        console.log('Login successful: \n' + email);
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
  fetch('http://'+fetch_address+':5001/contact_us', {
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

function setButtonActiveState(buttonId, isActive) {
  const btn = document.getElementById(buttonId);
  if (!btn) return;
  if (isActive) {
    btn.classList.add('active');
  } else {
    btn.classList.remove('active');
  }
}

function toe_off_click(settingNumbers) {
  const button = document.getElementById('toe_off');
  if (toe_off) {
    toe_off = false;
    setButtonActiveState('toe_off', true);
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true;
    });
  } else {
    toe_off = true;
    setButtonActiveState('toe_off', false);
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = false;
    });
    clear = true;
    setButtonActiveState('clear', false);
    document.getElementById("clear").innerText = "Select All";
  }
  select_button_check();
  select_checkbox();
}

function full_flight_click(settingNumbers) {
  const button = document.getElementById('full_flight');
  if (full_flight) {
    full_flight = false;
    setButtonActiveState('full_flight', true);
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true;
    });
  } else {
    full_flight = true;
    setButtonActiveState('full_flight', false);
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = false;
    });
    clear = true;
    setButtonActiveState('clear', false);
    document.getElementById("clear").innerText = "Select All";
  }
  select_button_check();
  select_checkbox();
}

function touch_down_click(settingNumbers) {
  const button = document.getElementById('touch_down');
  if (touch_down) {
    touch_down = false;
    setButtonActiveState('touch_down', true);
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true;
    });
  } else {
    touch_down = true;
    setButtonActiveState('touch_down', false);
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = false;
    });
    clear = true;
    setButtonActiveState('clear', false);
    document.getElementById("clear").innerText = "Select All";
  }
  select_button_check();
  select_checkbox();
}

function full_support_click(settingNumbers) {
  const button = document.getElementById('full_support');
  if (full_support) {
    full_support = false;
    setButtonActiveState('full_support', true);
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = true;
    });
  } else {
    full_support = true;
    setButtonActiveState('full_support', false);
    settingNumbers.forEach(number => {
      document.getElementById(`setting${number}`).checked = false;
    });
    clear = true;
    setButtonActiveState('clear', false);
    document.getElementById("clear").innerText = "Select All";
  }
  select_button_check();
  select_checkbox();
}

function clear_click() {
  const button = document.getElementById('clear');
  const settings = document.querySelectorAll('input[type="checkbox"]');
  if (clear) {
    clear = false;
    setButtonActiveState('clear', true);
    settings.forEach(setting => {
      setting.checked = true;
    });
    document.getElementById("clear").innerText = "Clear All";
    full_support = false;
    setButtonActiveState('full_support', true);
    full_flight = false;
    setButtonActiveState('full_flight', true);
    touch_down = false;
    setButtonActiveState('touch_down', true);
    toe_off = false;
    setButtonActiveState('toe_off', true);
  } else {
    clear = true;
    setButtonActiveState('clear', false);
    settings.forEach(setting => {
      setting.checked = false;
    });
    document.getElementById("clear").innerText = "Select All";
    full_support = true;
    setButtonActiveState('full_support', false);
    full_flight = true;
    setButtonActiveState('full_flight', false);
    touch_down = true;
    setButtonActiveState('touch_down', false);
    toe_off = true;
    setButtonActiveState('toe_off', false);
  }
  // check_radio();
}

function select_button_check() {
  if (!(toe_off || full_flight || touch_down || full_support)) {
    setButtonActiveState('clear', true);
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
function SendDrawData(event) {

  event.preventDefault(); // Stop form from submitting the traditional way
  const resultSection = document.getElementById('result');
  const video = document.getElementById('video-player');
  const source = document.getElementById('video-source');
  const downoadvideolink = document.getElementById('downloadResultVideo');
  const downloadcsvlink = document.getElementById('downloadResultCSV');


  resultSection.style.display = 'none'; // Hide the result section initially
  video.style.display = 'none'; // Hide the video player initially
  source.src = ""; // Clear the video source
  downoadvideolink.href = ""; // Clear the download link for the video
  downloadcsvlink.href = ""; // Clear the download link for the CSV

  const loading = document.getElementById('parent-container');
  const loading2 = document.getElementById('loading');

  // Show the loading GIF
  loading.style.display = 'block';
  loading2.style.display = 'block';

  const settings_colors = {};

  for (let i = 1; i <= 14; i++) {
    const checkbox = document.getElementById(`setting${i}`);
    const colorInput = document.getElementById(`colorSetting${i}`);
    settings_colors[document.getElementById(`setting${i}`).value] = [checkbox.checked, hexToRgb(colorInput.value)];
  }
  
  // Send the data to the server
  fetch('http://'+fetch_address+':5001/draw_analysis', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ settings_colors })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.response) {
        // Hide the loading GIF
        loading.style.display = 'none';
        loading2.style.display = 'none';

        resultSection.style.display = 'block'; // Show the result section
        downoadvideolink.href = "download_video/"+data.videoaddress; // Set the download link for the video
        downloadcsvlink.href = "download_csv/"+data.csvaddress; // Set the download link

        //Show reslut videos
        source.src = "video/"+data.videoaddress; // Set the video source to the received address
        video.load();
        video.style.display = 'block';
        video.play();
      } else {
        alert('Data sent failed');
        // Hide the loading GIF
        loading.style.display = 'none';
        loading2.style.display = 'none';
        resultSection.style.display = 'none'; // Hide the result section
        downoadvideolink.href = ""; // Clear the download link for the video
        downloadcsvlink.href = ""; // Clear the download link for the CSV
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert("Data sent failed".error.message);
      // Hide the loading GIF
      loading.style.display = 'none';
      loading2.style.display = 'none';
      resultSection.style.display = 'none'; // Hide the result section
      downloadcsvlink.href = ""; // Clear the download link for the CSV
      downoadvideolink.href = ""; // Clear the download link for the video
    });
}

let uploaded_video_name = null;

// Send and receive data from server and work with API
function SendVideo_height(event) {

  event.preventDefault(); // Stop form from submitting the traditional way
  // check_radio();
  if (document.getElementById('videoUpload').files.length == 0) {
    alert("You didn't upload video.");
    uploaded_video_name = null;
    return;
  }


  const loading = document.getElementById('parent-container-uploadvideo');
  const loading2 = document.getElementById('loading-uploadvideo');
  
  // Get the form element
  const form = document.getElementById('uploadForm');
  // Create a new FormData object
  const formData = new FormData(form);
  // Get runnerName from input field
  const runnerName = document.getElementById('runnerName').value.trim();
  // Check if runnerName is valid
  if (runnerName === "") {
    alert("Please enter a valid runner name.");
    loading.style.display = 'none';
    loading2.style.display = 'none';
    uploaded_video_name = null;
    return;
  }
  // Append the runnerName to the formData
  formData.append('runnerName', runnerName);
  // Get the runnerGender from the select field
  const runnerGender = document.querySelector('input[name="runnerGender"]:checked').value;
  // Append the runnerGender to the formData
  formData.append('runnerGender', runnerGender);
  // Get height_runner from the input fields (feet and inches)
  const feet = parseInt(document.getElementById('heightFeet').value) || 0;
  const inches = parseInt(document.getElementById('heightInches').value) || 0;
  // Convert to total inches for backend, or you can convert to meters if needed
  const height_runner = (feet * 12 + inches)*0.0254; // Convert to meters (1 inch = 0.0254 meters)
  // Check if height_runner is valid
  if (isNaN(height_runner) || height_runner <= 0) {
    alert("Please enter a valid height.");
    loading.style.display = 'none';
    loading2.style.display = 'none';
    uploaded_video_name = null;
    return;
  }
  // Get selected AI model (radio buttons)
  // const selectedModel = document.querySelector('input[name="model"]:checked').value;
  const selectedModel = "mediapipe";
  // Get usrname from usernameeDisplay span
  const username = document.getElementById('usernameDisplay').innerText;
  
  //Append the height_runner, selectedModel, and settings_colors to the formData
  formData.append('height_runner', height_runner);
  formData.append('selectedModel', selectedModel);
  // formData.append('settings_colors', JSON.stringify(settings_colors));
  formData.append('username', username);

  // Show the loading GIF
  loading.style.display = 'block';
  loading2.style.display = 'block';
  // Get upload and analysis sections id
  const upload_section = document.getElementById('upload-section');
  const analysis_section = document.getElementById('analysis-section');
  
  // Send the data to the server
  fetch('http://'+fetch_address+':5001/run_analysis', {
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
        uploaded_video_name = data.videoaddress; // Store the uploaded video name
        // Hide upload section and show analysis section
        upload_section.style.display = 'none';
        analysis_section.style.display = 'block';
        //Show reslut video
        console.log(data.message);
      } else {
        alert('Data sent failed');
        console.log(data.message);
        // Hide the loading GIF
        loading.style.display = 'none';
        loading2.style.display = 'none';
        upload_section.style.display = 'block';
        analysis_section.style.display = 'none';
        // resultVideoPreview.style.display = 'none';
      }
    })
    .catch(error => {
      console.error('Error:', error);
      // Hide the loading GIF
      loading.style.display = 'none';
      loading2.style.display = 'none';
      upload_section.style.display = 'block';
      analysis_section.style.display = 'none';
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


// add listener to profile page to get user details when page load
document.addEventListener('DOMContentLoaded', function () {
  // extract username from url
  const urlParams = new URLSearchParams(window.location.search);
  const username = urlParams.get('username') || 'No-Profile';
  // Update span for show username
  document.getElementById("usernameDisplay").innerText = username;
});

function handelViewProfileButton(event) {
  const username = document.getElementById('usernameDisplay').innerText;
  console.log(username);
  window.location.href = `http://${fetch_address}:5001/profile?username=${encodeURIComponent(username)}`;
}

// handeler for logout button
function handelLogoutButton(){
  window.location.href = `http://${fetch_address}:5001/`;
  // Clear the local storage
  localStorage.clear();
  // Clear the session storage
  sessionStorage.clear();
}


async function handleChatBotButton(event){
  let userInput = document.getElementById("user-input").value.trim();
  // Check if the input is empty
  if (userInput === "") {
    // alert("Please enter a message.");
    return;
  }

  // Get username and current date and time
  const username = document.getElementById("usernameDisplay").innerText;
  const dateTime = new Date().toLocaleString();

  // Make conversation history
  let conversationMessage = [];
  conversationMessage.push({ role: "user", content: userInput, username: username, dateTime: dateTime });

  let chatBox = document.getElementById("chat-box");

  // Add user message to chat
  let userMessage = document.createElement("div");
  userMessage.classList.add("chat-message", "user-message");
  userMessage.textContent = userInput;
  chatBox.appendChild(userMessage);
  // Simulated bot response
  let botMessage = document.createElement("div");
  botMessage.classList.add("chat-message", "bot-message");
  botMessage.textContent = "Thinking...";
  chatBox.appendChild(botMessage);

  // Clear input field
  document.getElementById("user-input").value = "";

  // Scroll to the latest message
  chatBox.scrollTop = chatBox.scrollHeight;
  // Send user input to server and get response
  fetch('http://' + fetch_address + ':5001/chat', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: conversationMessage }),
})
.then(async response => {
    const contentType = response.headers.get("content-type");

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    if (!contentType || !contentType.includes("application/json")) {
        const text = await response.text(); // This is likely HTML
        throw new Error(`Expected JSON, got HTML: ${text.slice(0, 100)}...`);
    }

    return response.json();
})
.then(data => {
    botMessage.textContent = data.answer;
})
.catch(error => {
    console.error("Error during fetch:", error);
    if (error.message.includes("JSON") || error.message.includes("<!doctype")) {
        botMessage.textContent = "Server error: Response is not valid JSON.";
    } else {
        botMessage.textContent = error.message === "timeout" ? "Server timeout." : "Unable to connect to the server.";
    }
});

  // Scroll to the latest message
  chatBox.scrollTop = chatBox.scrollHeight;
}

function handleKeyPressChatBot(event) {
  if (event.key === 'Enter') {
    handleChatBotButton();
  }
}


let currentlyVisibleImg = null;
let currentlyActiveBtn = null;

function hideAllSettingImages() {
  document.querySelectorAll('.setting-image').forEach(img => img.style.display = 'none');
  document.querySelectorAll('.visibility-btn').forEach(btn => btn.classList.remove('active-btn'));
  currentlyVisibleImg = null;
  currentlyActiveBtn = null;
}

document.querySelectorAll('.visibility-btn').forEach(button => {
  button.addEventListener('click', function (e) {
    e.stopPropagation();
    const imgId = this.getAttribute('data-img');
    const img = document.getElementById(imgId);

    if (currentlyVisibleImg && currentlyVisibleImg !== img) {
      hideAllSettingImages();
    }

    if (img.style.display === 'block') {
      img.style.display = 'none';
      this.classList.remove('active-btn');
      currentlyVisibleImg = null;
    } else {
      hideAllSettingImages();

      // Position popup near button
      const rect = this.getBoundingClientRect();
      img.style.top = `${this.offsetTop + 35}px`;  // below the button
      img.style.left = `${this.offsetLeft}px`;
      img.style.display = 'block';

      this.classList.add('active-btn');
      currentlyVisibleImg = img;
    }
  });
});

// Hide if clicking outside
document.addEventListener('click', function (e) {
  if (!e.target.closest('.visibility-btn') && !e.target.classList.contains('setting-image')) {
    hideAllSettingImages();
  }
});

function UplaodNewVideo() {
  // Reset all checkboxes
  for (let i = 1; i <= 11; i++) {
    const checkbox = document.getElementById(`setting${i}`);
    if (checkbox) checkbox.checked = false;
    const colorInput = document.getElementById(`colorSetting${i}`);
    if (colorInput) 
      {
        colorInput.selectedIndex = 0; // Reset to default color
        colorInput.style.backgroundColor = 'rgba(255, 0, 0, 0.2)'; // Reset color to default
        // colorInput.value = '#ff0000'; // Reset value to default
      }
  }
  for (let i = 12; i <= 14; i++) {
    const checkbox = document.getElementById(`setting${i}`);
    if (checkbox) checkbox.checked = false;
    const colorInput = document.getElementById(`colorSetting${i}`);
    if (colorInput)
      {
        // colorInput.value = '#00ff00'; // or your default color
        colorInput.style.backgroundColor = 'rgba(0, 255, 0, 0.2)'; // Reset color to default
        colorInput.selectedIndex = 2; // Reset to default color
      }
  }

  // Reset upload form
  const form = document.getElementById('uploadForm');
  if (form) form.reset();

  // Hide analysis/result sections, show upload section
  const upload_section = document.getElementById('upload-section');
  const analysis_section = document.getElementById('analysis-section');
  const result_section = document.getElementById('result');
  if (upload_section) upload_section.style.display = 'block';
  if (analysis_section) analysis_section.style.display = 'none';
  if (result_section) result_section.style.display = 'none';

  // Hide video preview if present
  const videoPreview = document.getElementById('videoPreview');
  if (videoPreview) {
    videoPreview.src = '';
    videoPreview.style.display = 'none';
  }

  // Reset any global state variables if needed
  uploaded_video_name = null;
}

// // Attach to button
// const uploadNewVideoBtn = document.getElementById('UplaodNewVideo');
// if (uploadNewVideoBtn) {
//   uploadNewVideoBtn.addEventListener('click', UplaodNewVideo);
// }

function FillHistoryTable(username){
  console.log("FillHistoryTable");
  const tableBody = document.getElementById('historyTableBody');
  // Clear existing rows
  tableBody.innerHTML = '';
  fetch('http://'+fetch_address+':5001/get_user_history', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.response)
      {
        if (Array.isArray(data.history) && data.history.length > 0) {
          populateVideoTable(data.history, tableBody);
        } else {
          alert('You do not have any history yet.');
          return;
        }
      }else{
        console.log(data.message);
        alert('You do not have any history yet.');
        return;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function populateVideoTable(videoList, tableBody) {
  // Clear the table body first
  tableBody.innerHTML = '';

  videoList.forEach(item => {
    const row = document.createElement("tr");

    // Video Name
    const nameCell = document.createElement("td");
    nameCell.textContent = item.video_name;
    row.appendChild(nameCell);

    // Timestamp
    const timeCell = document.createElement("td");
    timeCell.textContent = item.timestamp;
    row.appendChild(timeCell);

    // Original Video Link
    const videoLinkCell = document.createElement("td");
    const videoLink = document.createElement("a");
    videoLink.href = '/' + item.video_link;
    videoLink.textContent = "Download";
    videoLink.target = "_blank";
    videoLinkCell.appendChild(videoLink);
    row.appendChild(videoLinkCell);

    // Analyzed Result Links
    const resultCell = document.createElement("td");
    if (item.result_link && item.result_link.length > 0) {
      const ul = document.createElement("ul");
      item.result_link.forEach(link => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = '/' + link;
        a.textContent = "Run " + (item.result_link.indexOf(link) + 1);
        a.target = "_blank";
        li.appendChild(a);
        ul.appendChild(li);
      });
      resultCell.appendChild(ul);
    } else {
      resultCell.textContent = "No results yet";
    }
    row.appendChild(resultCell);

    // Action Button Column
    const actionCell = document.createElement("td");
    const actionBtn = document.createElement("button");
    actionBtn.textContent = "Re-Run";
    actionBtn.onclick = () => handleRunAction(item); // call your function with item
    actionCell.appendChild(actionBtn);
    row.appendChild(actionCell);

    // Append the row to the table body
    tableBody.appendChild(row);
  });
}

// Manage Tabs
function openTab(tabId) {
      // Hide all tab contents
      const contents = document.querySelectorAll('.tab-content');
      contents.forEach(content => content.classList.remove('active'));

      // Remove active class from all buttons
      const buttons = document.querySelectorAll('.tab-buttons button');
      buttons.forEach(button => button.classList.remove('active'));

      // Show selected tab content and mark button as active
      document.getElementById(tabId).classList.add('active');
      document.querySelector(`.tab-buttons button[onclick="openTab('${tabId}')"]`).classList.add('active');
}