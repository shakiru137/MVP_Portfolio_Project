// Function to toggle the visibility of the password-field
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

// Function to toggle the visibility of the confirm password field
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

// Function to validate the form fields before submission
function validateForm() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;
  const errorElement = document.getElementById("password-error");

  if (password !== confirmPassword) {
    errorElement.style.display = "block";
    return false;
  } else {
    errorElement.style.display = "none";
    return true;
  }
}

document.addEventListener(
  "touchstart",
  function (event) {
    if (event.touches.length > 1) {
      event.preventDefault();
    }
  },
  { passive: false }
);

document.addEventListener("gesturestart", function (event) {
  event.preventDefault();
});

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("confirmNameButton")
    .addEventListener("click", async function () {
      const recipientNumber = document.getElementById("recipient_number").value;
      if (recipientNumber) {
        try {
          const response = await fetch("/fetch_account_name", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ account_number: recipientNumber }),
          });
          const result = await response.json();
          if (response.ok) {
            document.getElementById("recipient_name").value =
              result.account_name;
          } else {
            document.getElementById("recipient_name").value = "";
          }
        } catch (error) {
          console.error("Error fetching account name:", error);
        }
      } else {
        document.getElementById("recipient_name").value =
          "Please enter recipient account number!";
      }
    });
});

document.addEventListener("DOMContentLoaded", function () {
  const confirmNameButton = document.getElementById("confirmNameButton");
  const sendButton = document.getElementById("sendButton");
  const pinSection = document.getElementById("pinSection");
  const createPinSection = document.getElementById("createPinSection");

  confirmNameButton.addEventListener("click", function () {
    const recipientNumber = document.getElementById("recipient_number").value;

    fetch("/fetch_account_name", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ account_number: recipientNumber }),
    })
      .then((response) => response.json())
      .then((data) => {
        const recipientNameInput = document.getElementById("recipient_name");
        recipientNameInput.value = data.account_name;
        if (data.account_name !== "Not Found!") {
          pinSection.classList.remove("hidden");
          pinSection.classList.add("slide-up");
        } else {
          pinSection.classList.add("hidden");
        }
      })
      .catch((error) => console.error("Error fetching account name:", error));
  });

  sendButton.addEventListener("click", function (event) {
    const pin = document.getElementById("pin").value;
    const createPin = document.getElementById("create_pin").value;
    const confirmPin = document.getElementById("confirm_pin").value;

    if (!pin && (!createPin || !confirmPin)) {
      event.preventDefault();
      createPinSection.classList.remove("hidden");
      pinSection.classList.add("hidden");
      createPinSection.classList.add("slide-up");
    }
  });
});
