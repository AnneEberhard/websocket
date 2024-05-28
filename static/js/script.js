const activeUser = document.currentScript.getAttribute("data-username");
const csrfToken = document.currentScript.getAttribute("data-csrf-token");

async function sendMessage() {
  let fd = new FormData();
  let token = csrfToken;
  let user = activeUser;
  fd.append("textmessage", messageField.value);
  fd.append("csrfmiddlewaretoken", token);
  try {
    renderSendingMessage(messageField.value, user);
    let response = await fetch("/chat/", {
      method: "POST",
      body: fd,
    });
    let jsonText = await response.json();
    let json = JSON.parse(jsonText);
    renderSentMessage(
      json["fields"]["text"],
      json["fields"]["author"],
      json["fields"]["created_at"]
    );
  } catch (e) {
    console.log("Error:", e);
    renderMessageNotSent(messageField.value, user);
  }
}

function getCurrentFormattedDate() {
  const options = {
    month: "short",
    day: "numeric",
    year: "numeric",
  };
  const currentDate = new Date();
  const formattedDate = currentDate.toLocaleDateString("en-US", options);
  const monthWithDot = formattedDate.replace(/^(\w+)( \d+, \d+)$/, "$1.$2");
  return monthWithDot;
}

function renderSendingMessage(newMessageText, user) {
  const formattedDate = getCurrentFormattedDate();
  messageContainer.innerHTML += `
      <div id="deleteMessage" class="messageBox authorMessage sendingMessage">
        <span class="colorGrey">[${formattedDate}] </span>${user}: <i class="colorGrey">${newMessageText}</i>
      </div>`;
}

function renderSentMessage(newMessageText, user, createdAt) {
  const formattedDate = getCurrentFormattedDate(new Date(createdAt));
  document.getElementById("deleteMessage").remove();
  messageContainer.innerHTML += `
    <div class="messageBox authorMessage">
    <span class="colorGrey">[${formattedDate}] </span>${user}: <i>${newMessageText}</i>
    </div>`;
  messageField.value = "";
}

function renderMessageNotSent(newMessageText, user) {
  const formattedDate = getCurrentFormattedDate();
  document.getElementById("deleteMessage").remove();
  messageContainer.innerHTML += `
    <div class="messageBox authorMessage messageNotSent">
    <span class="colorGrey">[${formattedDate}] </span>${user}: <i class="colorRed">${newMessageText} (Message not sent)</i>
    </div>`;
}

async function handleLogin() {
  let formElements = ["username", "password"];
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let fd = new FormData();
  let token = csrfToken;
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
  let fd = new FormData();
  let token = csrfToken;
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