const activeUser = document.currentScript.getAttribute("data-username");

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

function disableFields(elementsArray) {
  elementsArray.forEach((element) => {
    document.getElementById(element).disabled = true;
    document.getElementById(element).classList.add("disabled");
  });
}

function enableFields(elementsArray) {
  elementsArray.forEach((element) => {
    document.getElementById(element).disabled = false;
    document.getElementById(element).classList.remove("disabled");
  });
}

function errorMessage(divId, elementsArray) {
  document.getElementById(divId).style.display = "block";
  elementsArray.forEach((element) => {
    document.getElementById(element).value = "";
  });
}

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

function clearErrorMessage(divId) {
  document.getElementById(divId).style.display = "none";
}

function validatePassword(password) {
  if (password.length < 8) {
    return false;
  }
  if (!/[a-zA-Z]/.test(password)) {
    return false;
  }
  return true;
}

function  clearPasswortFields() {
  document.getElementById('password').value = "";
  document.getElementById('repeat_password').value = "";
}