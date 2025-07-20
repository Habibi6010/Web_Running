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

// add listener to VideoLog page to get user details when page load and fill labels and history table
document.addEventListener('DOMContentLoaded', function () {
  // extract username from url
  const urlParams = new URLSearchParams(window.location.search);
  const username = urlParams.get('username') || 'Profile';
  const useremail = urlParams.get('useremail') || 'Email';

  // Update span for show username
  document.getElementById("useremailDisplay").innerText = useremail;
  document.getElementById("usernameDisplay").innerText = username;
  // Set the link to dashboard links
  const dashboardLink1 = document.getElementById("doshboardlink1");
  if (dashboardLink1) {
    dashboardLink1.href = `http://${fetch_address}:5001/dashboard?username=${encodeURIComponent(username)}&useremail=${encodeURIComponent(useremail)}`;
  }
  const dashboardLink2 = document.getElementById("dashboardlink2");
  if (dashboardLink2) {
    dashboardLink2.href = `http://${fetch_address}:5001/dashboard?username=${encodeURIComponent(username)}&useremail=${encodeURIComponent(useremail)}`;
  }
  FillHistoryTable(useremail);
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
        let username = data.username;
        let useremail = data.useremail;
        window.location.href = `http://${fetch_address}:5001/dashboard?username=${encodeURIComponent(username)}&useremail=${encodeURIComponent(useremail)}`;
        console.log('Login successful: \n' + email);
      }
      else {
        alert('Login failed: \n' + 'Invalid email or password.' + '\nYour account may be inactive.');
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
    data ={email}
    fetch('http://'+fetch_address+':5001/forget_password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
          alert(data.message);
      })
      .catch(error => {
        alert("Server Error"+error.message);
      });
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
  const video = document.getElementById('videoPreview');
  const source = document.getElementById('videoSource');

  if (fileInput.files && fileInput.files[0]) {
    const fileURL = URL.createObjectURL(fileInput.files[0]);
    source.src = fileURL;
    video.style.display = "block";
    video.load();
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
  const video_id = document.getElementById('displayVideoID').innerText;
  const userEmail = document.getElementById('useremailDisplay').innerText;
  const runnerHeight = document.getElementById('displayRunnerHeight').innerText;
  // Send the data to the server
  fetch('http://'+fetch_address+':5001/draw_analysis', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ "settings_colors":settings_colors, "video_id":video_id, "userEmail":userEmail,"runner_height":runnerHeight})
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
        console.log(data.message);
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

// Send and receive data from server and work with API for sending video and get analysis
function SendVideo(event) {
  event.preventDefault(); // Stop form from submitting the traditional way
  // check_radio();
  if (document.getElementById('videoUpload').files.length == 0) {
    alert("You didn't upload video.");
    return;
  }
  // Show loading gif
  const loading = document.getElementById('parent-container-uploadvideo');
  const loading2 = document.getElementById('loading-uploadvideo');
  //Set runner info. text
  document.getElementById('displayRunnerName').innerText = document.getElementById('runnerName').value.trim();
  document.getElementById('displayRunnerID').innerText = document.getElementById('runnerIDNumber').value.trim();
  document.getElementById('displayRunnerGender').innerText = document.querySelector('input[name="runnerGender"]:checked').value;
  const feet = parseInt(document.getElementById('heightFeet').value) || 0;
  const inches = parseInt(document.getElementById('heightInches').value) || 0;
  document.getElementById('displayRunnerHeight').innerText = feet + "'" + inches + '"';
  // Get the form element
  const form = document.getElementById('uploadForm');
  // Create a new FormData object and append the form data
  const formData = new FormData(form);
  const userEmail = document.getElementById('useremailDisplay').innerText;
  const runnerID = document.getElementById('runnerIDNumber').value.trim();

  formData.append('selectedModel', "mediapipe");
  formData.append('userEmail', userEmail);
  formData.append('runnerID', runnerID);

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
        // Hide the loading GIF
        loading.style.display = 'none';
        loading2.style.display = 'none';
        // Hide upload section and show analysis section
        upload_section.style.display = 'none';
        analysis_section.style.display = 'block';
        //Show reslut video
        console.log(data.message);
        // set video info. text
        document.getElementById('displayVideoName').innerText = data.video_name;
        document.getElementById('displayVideoID').innerText = data.video_id;
        document.getElementById('displayVideoDate').innerText = data.upload_date;

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
// Listen for page load to fill the analysis page with data from local storage when redirect from rerun page
window.addEventListener("DOMContentLoaded", () => {
  const data = JSON.parse(localStorage.getItem("rerunData"));
  if (data && Object.keys(data).length > 0) {
    console.log("Page loaded, checking for rerun data...");
    // Reset the upload form and settings
    UplaodNewVideo();
    // Show the analysis section and hide others
    document.getElementById('upload-section').style.display = 'none';
    document.getElementById('analysis-section').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    // Fill the fields
    document.getElementById("displayVideoName").innerText = data.video_name;
    document.getElementById("displayVideoID").innerText = data.video_id;
    document.getElementById("displayVideoDate").innerText = data.timestamp;

    document.getElementById("displayRunnerName").innerText = data.runner_name;
    document.getElementById("displayRunnerID").innerText = data.runner_id;
    document.getElementById("displayRunnerGender").innerText = data.runner_gender;
    document.getElementById("displayRunnerHeight").innerText = data.runner_height;

    // Optionally clear after loading
    localStorage.removeItem("rerunData");
  }
});
// add listener to profile page to get user details when page load
document.addEventListener('DOMContentLoaded', function () {
  // extract username from url
  const urlParams = new URLSearchParams(window.location.search);
  const useremail = urlParams.get('useremail') || 'No-email';
  const username = urlParams.get('username') || 'Profile';
  // Update span for show username
  document.getElementById("useremailDisplay").innerText = useremail;
  document.getElementById("usernameDisplay").innerText = username;
});

function handelVideLogButton(event) {
  const useremail = document.getElementById('useremailDisplay').innerText;
  const username = document.getElementById('usernameDisplay').innerText;

  console.log(username);
  window.location.href = `http://${fetch_address}:5001/videolog?useremail=${encodeURIComponent(useremail)}&username=${encodeURIComponent(username)}`;
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
  const username = document.getElementById("useremailDisplay").innerText;
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

  // Reset runner info
  document.getElementById("runnerIDNumber").value = "";
  document.getElementById("runnerIDNumber").disabled = false; // enable the runner ID field
  document.getElementById("nextbutton").disabled = false; // enable the submit button
  document.getElementById("TabDiv").style.display = "none"; // hide the edit button
  const autofillresult = document.getElementById("autofillResult");
  autofillresult.innerText = "For quick search enter runner ID number.";
  autofillresult.style.color = "green";
  RunnerInfoFieldsClear();
  RunnerInfoFeildsDisabled(false); // allow editing
  // Reset score inputs
  const scoreInputs= document.querySelectorAll('input[name="enterscore"]');
  scoreInputs.forEach(input => input.value = "");
}

function FillHistoryTable(userEmail){
  console.log("FillHistoryTable");
  const tableBody = document.getElementById('historyTableBody');
  // Clear existing rows
  tableBody.innerHTML = '';
  fetch('http://'+fetch_address+':5001/get_user_history', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ "userEmail": userEmail })
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

    // Runner Name
    const nameCell = document.createElement("td");
    nameCell.textContent = item.runner_name;
    row.appendChild(nameCell);
   
    // Timestamp
    const timeCell = document.createElement("td");
    timeCell.textContent = item.timestamp;
    row.appendChild(timeCell);

    // Video Name and ID
    const idCell = document.createElement("td");
    idCell.innerHTML = `${item.video_name} (ID: ${item.video_id})`;
    row.appendChild(idCell);
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
    actionBtn.onclick = () => handleRerunAction(item); // call your function with item
    actionCell.appendChild(actionBtn);
    row.appendChild(actionCell);

    // Append the row to the table body
    tableBody.appendChild(row);
  });
}
// Handle re-run action
function handleRerunAction(item) {
  console.log("Re-Run clicked for video ID:", item.video_id);
  // load video data into analysis section
  // go to analysis section
  const useremail = document.getElementById('useremailDisplay').innerText;
  const username = document.getElementById('usernameDisplay').innerText;
  // Save data to localStorage
  localStorage.setItem("rerunData", JSON.stringify({
    video_name: item.video_name,
    video_id: item.video_id,
    timestamp: item.timestamp,
    runner_name: item.runner_name,
    runner_id: item.runner_id,
    runner_gender: item.runner_gender,
    runner_height: item.runner_height,
    useremail: useremail,
    username: username
  }));
  console.log(username);
  window.location.href = `http://${fetch_address}:5001/dashboard?useremail=${encodeURIComponent(useremail)}&username=${encodeURIComponent(username)}`;
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

// set the category list based on selected environment
function updatecategorylist(selectedEnv){
    const optionList = document.getElementById("selectcategorizlist");
    const selectrunningevent = document.getElementById("selectrunningevent");
    optionList.innerHTML = ""; // clear old options
    selectrunningevent.innerHTML = ""; // clear old options
      let options = [];
      let event = [];
      if (selectedEnv === "indoor") {
        options = ["NCAA DIV. I", "NCAA DIV. II", "NCAA DIV. III","NAIA","NJCAA"];
        event = ["Sprint 60m", "Sprint 200m", "Sprint 400m", "Middle Distance 800m", "Middle Distance Mile (1609m) ", "Long Distance 3000m", "Long Distance 5000m"];
      } else if (selectedEnv === "outdoor") {
        options = ["NCAA DIV. I","NCAA DIV. II", "NCAA DIV. III", "NAIA","NJCAA DIV.I"];
        event = ["Sprint 100m", "Sprint 200m", "Sprint 400m", "Middle Distance 800m", "Middle Distance 1500m","Long Distance 5,000m", "Long Distance 10,000m"];
      }
      options.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt;
        option.textContent = opt;
        optionList.appendChild(option);
      });
      event.forEach(ev => {
        const option = document.createElement("option");
        option.value = ev;
        option.textContent = ev;
        selectrunningevent.appendChild(option);
      });
}
// Add score input field dynamically
function addScoreInput(){
  const container = document.getElementById('scoreContainer');
  const input = document.createElement('input');
  input.type = 'text';
  input.name = 'enterscore';
  input.title="Fromat: m:ss.xx (e.g., 1:23.45) or s.xx (e.g., 12.34)"
  input.style.width = '80px';
  input.required = true;
  container.appendChild(input);
  attachValidation(input);
}

function ScoreHelp(){
  alert("To add multiple scores, click the '+Add Score' button.\nEach click will add a new input field for entering another score.\n\nFormat for each field is time in \nminutes:seconds.milliseconds (e.g., 4:30.52).\nor\nseconds.milliseconds (e.g., 10.52).");
}

// Validation pattern: m:ss.xx or s.xx for input score fields
const pattern = /^(\d+:\d{2}\.\d{2}|\d+\.\d{2}|\d+\.\d|\d|\d{2})$/;
const inputs = document.querySelectorAll('input[name="enterscore"]');
inputs.forEach(input => attachValidation(input));
// Attach validation to new input field
function attachValidation(input) {
  input.addEventListener('blur', () => {
    const value = input.value.trim();
    if (value && !pattern.test(value)) {
      input.value = "";
      input.classList.add('invalid');
    } else {
      input.classList.remove('invalid');
    }
  });

  input.addEventListener('input', () => {
    if (pattern.test(input.value.trim())) {
      input.classList.remove('invalid');
    }
  });
}


// Send and receive data from server and work with API for sending score and get rank
function SendScores(event) {

  event.preventDefault(); // Stop form from submitting the traditional way
  // Get all data from the HTML page
  const userEmail = document.getElementById('useremailDisplay').innerText;
  const runnerID = document.getElementById('runnerIDNumber').value.trim();
  const season = document.querySelector('input[name="env"]:checked').value;
  const category = document.getElementById('selectcategorizlist').value;
  const selectedEvent = document.getElementById('selectrunningevent').value;
  const scoreInputs = document.querySelectorAll('input[name="enterscore"]');
  let scores = [];
  scoreInputs.forEach(input => {
    const value = input.value.trim();
    if (value) scores.push(value);
  });
  if (scores.length < 4 ) {
    alert("Please enter at least five valid score.");  
    return;
  }

  // Show the loading GIF
  const loading = document.getElementById('parent-container-uploadvideo');
  const loading2 = document.getElementById('loading-uploadvideo');
  
  loading.style.display = 'block';
  loading2.style.display = 'block';
  // Get upload and analysis sections id
  const upload_section = document.getElementById('upload-section');
  const analysis_section = document.getElementById('rankingResult-section');
  let dataToSend = {
    "userEmail": userEmail,
    "runnerID": runnerID,
    "season": season,
    "category": category,
    "selectedEvent": selectedEvent,
    "scores": scores
  };
  // Send the data to the server
  fetch('http://'+fetch_address+':5001/save_runner_score', {
    method: 'POST',
    body: JSON.stringify(dataToSend),
    headers: { 'Content-Type': 'application/json'} 
  })
    .then(response => response.json())
    .then(data => {
      if (data.response) {
        // Hide the loading GIF
        loading.style.display = 'none';
        loading2.style.display = 'none';
        // Hide upload section and show analysis section
        upload_section.style.display = 'none';
        analysis_section.style.display = 'block';
        // Fill the ranking result fields
        document.getElementById('displayRankRunnerName').innerText = document.getElementById('runnerName').value.trim();
        document.getElementById('displayRankRunnerID').innerText = runnerID;
        document.getElementById('displayRankRunnerGender').innerText = document.querySelector('input[name="runnerGender"]:checked').value;
        const feet = parseInt(document.getElementById('heightFeet').value) || 0;
        const inches = parseInt(document.getElementById('heightInches').value) || 0;
        document.getElementById('displayRankRunnerHeight').innerText = feet + "'" + inches + '"';
        document.getElementById('displayRankSeason').innerText = season;
        document.getElementById('displayRankCategory').innerText = category;
        document.getElementById('displayRankEvent').innerText = selectedEvent;
        document.getElementById('displaySubmittedScores').innerText = scores.join(", ");

        //Show reslut video
        console.log(data.message,data.score_id);
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

// Function to disable or enable the name,height, gender fiedls
function RunnerInfoFeildsDisabled(Active){
  if (Active){
    document.getElementById('runnerName').disabled = true;
    document.getElementById('heightFeet').disabled = true;
    document.getElementById('heightInches').disabled = true;
    document.getElementsByName('runnerGender').forEach(r => r.disabled = true);
  }
  else{
    document.getElementById('runnerName').disabled = false;
    document.getElementById('heightFeet').disabled = false;
    document.getElementById('heightInches').disabled = false;
    document.getElementsByName('runnerGender').forEach(r => r.disabled = false);
    document.getElementsByName('runnerGender').forEach(r => {if(r.value === "Male") r.checked = true});
  }
}
// Function to Clear runner info fields
function RunnerInfoFieldsClear() {
    document.getElementById('runnerName').value = '';
    document.getElementById('heightFeet').value = '';
    document.getElementById('heightInches').value = '';
    document.getElementsByName('runnerGender').forEach(r => r.checked = false);
}

function autoFillRunnerInfo(){
  const runnerID = document.getElementById("runnerIDNumber").value.trim();
  const userEmail = document.getElementById("useremailDisplay").innerText;
  const autofillresult = document.getElementById("autofillResult");
  // console.log(runnerID, userEmail);
  if (runnerID === ""){
    RunnerInfoFeildsDisabled(false); // allow editing
    return;
  }
  else{

    fetch('http://'+fetch_address+':5001/find_runner_info',{method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ runnerID: runnerID, userEmail: userEmail })
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            // Clear previous data
            RunnerInfoFieldsClear();
            // Fill the form
            document.getElementById('runnerName').value = data.name;
            document.getElementById('heightFeet').value = data.heightFeet;
            document.getElementById('heightInches').value = data.heightInches;

            const genderRadios = document.getElementsByName('runnerGender');
            genderRadios.forEach(radio => {
                radio.checked = (radio.value === data.gender);
            });
            autofillresult.innerText = "Runner info found and filled.";
            autofillresult.style.color = "green";
            RunnerInfoFeildsDisabled(true); // prevent editing
        } else {
            autofillresult.innerText = "Runner ID not found. Please enter the details manually.";
            autofillresult.style.color = "red";
            console.log(data.message);
            RunnerInfoFieldsClear();
            RunnerInfoFeildsDisabled(false); // allow editing
        }
    })
    .catch(error => {
        console.error('Error fetching runner info:', error);
        autofillresult.innerText = "Error fetching runner info. Please try again.";
        autofillresult.style.color = "red";
    });
  }
}

function RunnerInfoSubmit(event){
  event.preventDefault(); // Stop form from submitting the traditional way
  // Get the form element
  const form = document.getElementById('uploadForm');
  // Create a new FormData object
  const formData = new FormData(form);
  // Get runnerName from input field
  const runnerName = document.getElementById('runnerName').value.trim();
  // Check if runnerName is valid
  if (runnerName === "") {
    alert("Please enter a valid runner name.");
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
    return;
  }

  const useremail = document.getElementById('useremailDisplay').innerText;
  formData.append('ruunerHeightFeet', feet);
  formData.append('ruunerHeightInche', inches);
  formData.append('userEmail', useremail);
  const runnerID = document.getElementById("runnerIDNumber").value.trim();
  formData.append('runnerID', runnerID);

  const autofillresult = document.getElementById("autofillResult");
  autofillresult.innerText = "";
  // Send the data to the server
  fetch('http://'+fetch_address+':5001/save_runner_info', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.response) {
        autofillresult.innerText = data.message;
        autofillresult.style.color = "green";
        RunnerInfoFeildsDisabled(true); // prevent editing
        document.getElementById("runnerIDNumber").value = data.runnerID; // set the runner ID
        document.getElementById("runnerIDNumber").disabled = true; // disable the runner ID field
        document.getElementById("nextbutton").disabled = true; // disable the submit button
        document.getElementById("TabDiv").style.display = "block"; // show the edit button
      } else {
        autofillresult.innerText = data.message;
        autofillresult.style.color = "red";
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert("Failed to save runner information");
    });
}

function RunnerInfoClear(event){
  event.preventDefault();
  document.getElementById("runnerIDNumber").value = "";
  document.getElementById("runnerIDNumber").disabled = false; // enable the runner ID field
  document.getElementById("nextbutton").disabled = false; // enable the submit button
  document.getElementById("TabDiv").style.display = "none"; // hide the edit button
  const autofillresult = document.getElementById("autofillResult");
  autofillresult.innerText = "For quick search enter runner ID number.";
  autofillresult.style.color = "green";
  RunnerInfoFieldsClear();
  RunnerInfoFeildsDisabled(false); // allow editing
}

function handelViewProfileButton(){
  const useremail = document.getElementById('useremailDisplay').innerText;
  const username = document.getElementById('usernameDisplay').innerText;
  // Save data to localStorage
  localStorage.setItem("profilePage",JSON.stringify({"userName":username,"userEmail":useremail})); 
  window.location.href = `http://${fetch_address}:5001/profile`;
  
}


// Fill runner table in profile page
function FillRunnerTable(userEmail){
  console.log("FillRunnerTable");
  const tableBody = document.getElementById('runnerTableBody');
  // Clear existing rows
  tableBody.innerHTML = '';
  fetch('http://'+fetch_address+':5001/get_user_runners', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ "userEmail": userEmail })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.response)
      {
        if (Array.isArray(data.runners) && data.runners.length > 0) {
          populateRunnerTable(data.runners, tableBody);
        } else {
          alert('You do not have any runners yet.');
          return;
        }
      }else{
        console.log(data.message);
        return;
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function populateRunnerTable(runnerList, tableBody) {
  // Clear the table body first
  tableBody.innerHTML = '';

  runnerList.forEach(item => {
    const row = document.createElement("tr");

    // Runner ID
    const idCell = document.createElement("td");
    idCell.textContent = item.runner_id;
    row.appendChild(idCell);

    // Runner Name
    const nameCell = document.createElement("td");
    nameCell.textContent = item.name;
    row.appendChild(nameCell);
   
    // Creation Time
    const timeCell = document.createElement("td");
    timeCell.textContent = item.created_at;
    row.appendChild(timeCell);

    // Runner Gender
    const genderCell = document.createElement("td");
    genderCell.innerHTML =item.gender;
    row.appendChild(genderCell);

    // Runner Height
    const heightCell = document.createElement("td");
    heightCell.innerText = item.height
    row.appendChild(heightCell);

    // Append the row to the table body
    tableBody.appendChild(row);
  });
}

// Fill the profile page with user data from DB
function FillUserInfo(userEmail){
  console.log("FillUserInfon");
  fetch('http://'+fetch_address+':5001/get_user_info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ "userEmail": userEmail })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.response)
      {
        document.getElementById("username").value = data.full_name;
        document.getElementById("useremail").value = userEmail;
        document.getElementById("created_at").value = data.created_at;
        document.getElementById("user_role").value = data.role;
      }else{
        console.log(data.message);
        document.getElementById("username").value = "";
        document.getElementById("useremail").value = "";
        document.getElementById("created_at").value = "";
        document.getElementById("user_role").value = "";
        return;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      document.getElementById("username").value = "";
      document.getElementById("useremail").value = "";
      document.getElementById("created_at").value = "";
      document.getElementById("user_role").value = "";
    });
}

// Update user info from profile page
function updateProfile(){
  full_name = document.getElementById("username").value.trim();
  userEmali = document.getElementById("useremail").value.trim();
  role = document.getElementById("user_role").value.trim();
  if (full_name === "" || userEmali === "" || role === ""){
    alert("All fields are required");
    return;
  }
  fetch('http://'+fetch_address+':5001/update_user_info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ "full_name": full_name, "useremali": userEmali, "role":role })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.response)
      {
        alert(data.message);
      }else{
        alert(data.message);
        return;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert("Failed to update user info");
    });
    
}

// Change password from profile page
function changePassword(){
  const currentPassword = document.getElementById("oldpassword").value.trim();
  const newPassword = document.getElementById("newpassword").value.trim();
  const confirmNewPassword = document.getElementById("confirmpassword").value.trim();
  const userEmali = document.getElementById("useremail").value.trim();

  if (currentPassword === "" || newPassword === "" || confirmNewPassword === ""){
    alert("All fields are required");
    return;
  }
  if (newPassword !== confirmNewPassword){
    document.getElementById('passwordMatchMessage').innerText = "New password and confirm password do not match";
    document.getElementById('passwordMatchMessage').style.color = "red";
    return;
  }
  if (newPassword.length < 6){
    document.getElementById('passwordMatchMessage').innerText = "New password must be at least 6 characters long";
    document.getElementById('passwordMatchMessage').style.color = "red";
    return;
  }

  fetch('http://'+fetch_address+':5001/change_user_password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ "useremali": userEmali, "currentPassword": currentPassword, "newPassword": newPassword })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      if (data.response)
      {
        alert(data.message);
        // Clear the input fields
        document.getElementById("oldpassword").value = "";
        document.getElementById("newpassword").value = "";
        document.getElementById("confirmpassword").value = "";
        document.getElementById('passwordMatchMessage').innerText = "";

      }else{
        alert(data.message);
        document.getElementById('passwordMatchMessage').innerText = "";

        return;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert("Failed to change password");
    });
}

// Handle ranking log button
function handelrankLogButton(){
  alert("This feature is coming soon.");
}