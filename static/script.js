// Function to toggle the visibility of the password-field
function togglePasswordVisibility() {
  // Get the password input element by its ID
  const passwordInput = document.getElementById("password");

  // Get the eye icon element by its ID
  const eyeIcon = document.getElementById("eye-icon");

  // Check the current type of the password input field
  if (passwordInput.type === "password") {
    // If it's currently of type 'password', change it to 'text'
    passwordInput.type = "text";

    // Remove the 'fa-eye' class (which shows the eye icon) and add 'fa-eye-slash' (which shows the eye-slash icon)
    eyeIcon.classList.remove("fa-eye");
    eyeIcon.classList.add("fa-eye-slash");
  } else {
    // If it's currently of type 'text', change it back to 'password'
    passwordInput.type = "password";

    // Remove the 'fa-eye-slash' class and add 'fa-eye'
    eyeIcon.classList.remove("fa-eye-slash");
    eyeIcon.classList.add("fa-eye");
  }
}

// Function to toggle the visibility of the confirm password field
function toggleConfirmPasswordVisibility() {
  // Get the confirm password input element by its ID
  const confirmPasswordInput = document.getElementById("confirm_password");

  // Get the eye icon element for the confirm password field by its ID
  const eyeIcon = document.getElementById("confirm-eye-icon");

  // Check the current type of the confirm password input field
  if (confirmPasswordInput.type === "password") {
    // If it's currently of type 'password', change it to 'text'
    confirmPasswordInput.type = "text";

    // Remove the 'fa-eye' class and add 'fa-eye-slash'
    eyeIcon.classList.remove("fa-eye");
    eyeIcon.classList.add("fa-eye-slash");
  } else {
    // If it's currently of type 'text', change it back to 'password'
    confirmPasswordInput.type = "password";

    // Remove the 'fa-eye-slash' class and add 'fa-eye'
    eyeIcon.classList.remove("fa-eye-slash");
    eyeIcon.classList.add("fa-eye");
  }
}

// Function to validate the form fields before submission
function validateForm() {
  // Get the value of the password input field
  const password = document.getElementById("password").value;

  // Get the value of the confirm password input field
  const confirmPassword = document.getElementById("confirm_password").value;

  // Get the error element by its ID
  const errorElement = document.getElementById("password-error");

  // Check if the password and confirm password values match
  if (password !== confirmPassword) {
    // If they don't match, show the error message and prevent form submission
    errorElement.style.display = "block";
    return false; // Prevent form submission
  } else {
    // If they match, hide the error message and allow form submission
    errorElement.style.display = "none";
    return true; // Allow form submission
  }
}

document.addEventListener(
  "touchstart",
  function (event) {
    event.preventDefault();
  },
  { passive: false }
);

let startX = 0;

document.addEventListener(
  "touchstart",
  function (event) {
    startX = event.touches[0].clientX;
  },
  { passive: false }
);

document.addEventListener(
  "touchmove",
  function (event) {
    let moveX = event.touches[0].clientX;
    let diffX = moveX - startX;

    // Prevent default behavior if horizontal scroll is detected
    if (Math.abs(diffX) > 0) {
      event.preventDefault();
    }
  },
  { passive: false }
);
