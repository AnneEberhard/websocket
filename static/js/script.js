const activeUser = document.currentScript.getAttribute("data-username");

/**
 * Converts a string to a URL-friendly slug format by transforming it to lower case,
 * replacing spaces with hyphens, removing non-word characters, and eliminating 
 * multiple or trailing hyphens.
 *
 * @param {string} text - The string to be slugified.
 * @returns {string} The slugified string, suitable for URLs.
 */
function slugify(text) {
  return text.toString().toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+/, '')          
    .replace(/-+$/, '');            
}

/**
 * Handles the user login process by submitting username and password to the server,
 * and managing the response to either redirect the user or show an error message.
 * Disables the form fields during the request and re-enables them afterward.
 */
async function handleLogin() {
  let formElements = ["username", "password"];
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let token = document.querySelector('[name=csrfmiddlewaretoken]').value;
  let fd = new FormData();
  
  fd.append("username", username);
  fd.append("password", password);
  fd.append("csrfmiddlewaretoken", token);
  disableFields(formElements);
  try {
    let response = await fetch("/login/", {
      method: "POST",
      body: fd,
    });
    let json = await response.json();
    if (json.success) {
      window.location.href = json.redirect;
    } else {
      errorMessage("loginFailed", formElements);
    }
  } catch (e) {
    console.log("Error:", e);
  }
  enableFields(formElements);
}

/**
 * Disables the input fields and adds a 'disabled' class to them.
 * @param {Array<string>} elementsArray - An array of element IDs to be disabled.
 */
function disableFields(elementsArray) {
  elementsArray.forEach((element) => {
    document.getElementById(element).disabled = true;
    document.getElementById(element).classList.add("disabled");
  });
}

/**
 * Enables the input fields and removes the 'disabled' class from them.
 * @param {Array<string>} elementsArray - An array of element IDs to be enabled.
 */
function enableFields(elementsArray) {
  elementsArray.forEach((element) => {
    document.getElementById(element).disabled = false;
    document.getElementById(element).classList.remove("disabled");
  });
}

/**
 * Displays an error message and clears the values of specified input fields.
 * @param {string} divId - The ID of the div that displays the error message.
 * @param {Array<string>} elementsArray - An array of element IDs whose values will be cleared.
 */
function errorMessage(divId, elementsArray) {
  document.getElementById(divId).style.display = "block";
  elementsArray.forEach((element) => {
    document.getElementById(element).value = "";
  });
}

/**
 * Handles the user registration process by submitting registration data to the server,
 * validating the password, and managing the response to either redirect the user or show error messages.
 * Disables the form fields during the request and re-enables them afterward.
 * Uses various helper functions to validate data, manage UI messages, and gather form data.
 */
async function handleRegister() {
  let formElements = [
    "username",
    "email",
    "first_name",
    "last_name",
    "password",
    "repeat_password",
  ];
  fd = await getRegisterData();
  let password = fd.get("password");
  if (!validatePassword(password)) {
    errorMessage("passwordNoValidate", formElements);
    return;
  } else {
    clearErrorMessage("passwordNoValidate");
    clearPasswortFields();
    disableFields(formElements);
    try {
      let response = await fetch("/register/", {
        method: "POST",
        body: fd,
      });
      let json = await response.json();
      if (json.success) {
        window.location.href = json.redirect;
      } else {
        if (json.passwordNoMatch) {
          errorMessage("passwordNoMatch", formElements);
        } else {
          clearErrorMessage("passwordNoMatch");
        }
        if (json.error) {
          errorMessage("error", formElements);
        } else {
          clearErrorMessage("error");
        }
      }
    } catch (e) {
      console.log("Error:", e);
    }
    enableFields(formElements);
  }
}

/**
 * Collects and packages registration data from form fields into a FormData object.
 * @returns {FormData} A FormData object containing the user registration data.
 */
async function getRegisterData() {
  let username = document.getElementById("username").value;
  let email = document.getElementById("email").value;
  let first_name = document.getElementById("first_name").value;
  let last_name = document.getElementById("last_name").value;
  let password = document.getElementById("password").value;
  let repeat_password = document.getElementById("repeat_password").value;
  let token = document.querySelector('[name=csrfmiddlewaretoken]').value;
  let fd = new FormData();

  fd.append("username", username);
  fd.append("email", email);
  fd.append("first_name", first_name);
  fd.append("last_name", last_name);
  fd.append("password", password);
  fd.append("repeat_password", repeat_password);
  fd.append("csrfmiddlewaretoken", token);
  return fd;
}

/**
 * Hides the error message display for a given div.
 * @param {string} divId - The ID of the div where the error message is displayed.
 */
function clearErrorMessage(divId) {
  document.getElementById(divId).style.display = "none";
}

/**
 * Validates a password to ensure it meets specific criteria.
 * @param {string} password - The password to validate.
 * @returns {boolean} True if the password meets the criteria, false otherwise.
 */
function validatePassword(password) {
  if (password.length < 8) {
    return false;
  }
  if (!/[a-zA-Z]/.test(password)) {
    return false;
  }
  return true;
}

/**
 * Clears the password and repeat password fields on the form.
 */
function  clearPasswortFields() {
  document.getElementById('password').value = "";
  document.getElementById('repeat_password').value = "";
}
