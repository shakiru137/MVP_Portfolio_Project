function togglePasswordVisibility() {
  const passwordInput = document.getElementById("password");
  const eyeIcon = document.getElementById("eye-icon");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    eyeIcon.classList.remove("fa-eye");
    eyeIcon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    eyeIcon.classList.remove("fa-eye-slash");
    eyeIcon.classList.add("fa-eye");
  }
}

function toggleConfirmPasswordVisibility() {
  const confirmPasswordInput = document.getElementById("confirm_password");
  const eyeIcon = document.getElementById("confirm-eye-icon");

  if (confirmPasswordInput.type === "password") {
    confirmPasswordInput.type = "text";
    eyeIcon.classList.remove("fa-eye");
    eyeIcon.classList.add("fa-eye-slash");
  } else {
    confirmPasswordInput.type = "password";
    eyeIcon.classList.remove("fa-eye-slash");
    eyeIcon.classList.add("fa-eye");
  }
}

function validateForm() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;
  const errorElement = document.getElementById("password-error");

  if (password !== confirmPassword) {
    errorElement.style.display = "block";
    return false; // Prevent form submission
  } else {
    errorElement.style.display = "none";
    return true; // Allow form submission
  }
}
