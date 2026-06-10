import {getAcessToken, getCurrentUser, removeAcessToken} from "../script/auth.js"

const imageInput = document.querySelector(".js-image-input");
const preview = document.querySelector(".js-profile-preview");
const uploadImageButton = document.querySelector(".js-upload-image-button");
const username = document.querySelector(".js-username");
const email = document.querySelector(".js-email");
const updateProfileButton = document.querySelector(".js-update-profile");
const logOutButton = document.querySelector(".js-log-out");
const deleteAccountButton = document.querySelector(".js-delete-account-button");


let currentUser = null;

async function loadingUser() {
  currentUser = await getCurrentUser()
}


async function init() {

  await loadingUser()

  preview.src = currentUser.image_url
  username.value = currentUser.username
  email.value = currentUser.email

// IMAGE PREVIEW LOGIC

imageInput.addEventListener("change", () => {

  const file = imageInput.files[0];

  if (!file)
    return;


  if (file.size > 5 * 1024 * 1024){

  alert("Image exceeds 5MB");
  imageInput.value = "";
  return;

}

  preview.src = URL.createObjectURL(file);

  uploadImageButton.disabled = false;

 });


 // UPLOADING IMAGE LOGIC

 uploadImageButton.addEventListener("click", async (e) => {
  e.preventDefault()

  const file = imageInput.files[0];
  
  if (!file) return

  const formData = new FormData()
  formData.append("image", file)

  const token = getAcessToken()
  const currentUserId = Number(currentUser.id);

  try {

    const response = await fetch(`/api/users/${currentUserId}/picture`, {
    method: "PATCH",
    headers: {
      'Authorization': `Bearer ${token}`,
    },
      body: formData
    })

    if (!response.ok) {

      console.log(await response.json())
      return
    }

    alert("Profile image changed succefully")
    location.reload()

  } catch(error) {
    console.log("Please check your internet connection")
    alert("Please check your internet connection")
  }
  


 })



 // UPLOADING PROFILE DETAILS

 updateProfileButton.addEventListener("click", async (e) => {

  e.preventDefault()

  const token = getAcessToken()

  const changed = {
    username: username.value,
    email: email.value
  }
  
  const currentUserId = Number(currentUser.id);

  try {

    const response = await fetch(`/api/users/${currentUserId}`, {
    method: "PATCH",
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },

     body: JSON.stringify(changed)
    })

    if (!response.ok) {

      console.log(await response.json())
      return
    }

    alert("Profile changed succefully")
    location.reload()

  } catch(error) {
    console.log("Please check your internet connection")
    alert("Please check your internet connection")
  }
  

 })


const originalUsername = username.value;
const originalEmail = email.value;


function checkChanges() {

const changed = username.value !== originalUsername || email.value !== originalEmail;

updateProfileButton.disabled = !changed;

}


username.addEventListener("input", checkChanges);

email.addEventListener("input", checkChanges);



logOutButton.addEventListener('click', () => {

  removeAcessToken();
  location.href = "/"

})


deleteAccountButton.addEventListener("click", async (e) => {
  e.preventDefault()

  const token = getAcessToken()
  const currentUserId = Number(currentUser.id);

  try {

    const response = await fetch(`/api/users/${currentUserId}`, {
    method: "DELETE",
    headers: {
      'Authorization': `Bearer ${token}`,
    }
    })

    if (!response.ok) {
      console.log(await response.json())
      return
    }

    alert("Account succefully deleted")
    removeAcessToken()
    location.href = "/login"

  } catch(error) {
    console.log("Please check your internet connection")
    alert("Please check your internet connection")
  }
  

})







// PASSWORD UPDATING JS

const togglePasswordButton = document.querySelector(".js-change-password-toggle");
const passwordContainer = document.querySelector(".js-change-password-container");
const oldPasswordInput = document.querySelector(".js-old-password");
const newPasswordInput = document.querySelector(".js-new-password");
const confirmPasswordInput = document.querySelector(".js-confirm-password");
const submitPasswordButton = document.querySelector(".js-change-password-submit");
const passwordStatus = document.querySelector(".js-password-status");
const changePasswordForm = document.querySelector(".js-change-password-form");

/* ============================= */
/* TOGGLE FORM */
/* ============================= */

togglePasswordButton.addEventListener("click", () =>{
    passwordContainer.classList.toggle(
        "show"
    );
});
/* ============================= */
/* VALIDATION */
/* ============================= */

function validatePasswordForm(){

    const oldPassword = oldPasswordInput.value.trim();
    const newPassword = newPasswordInput.value.trim();
    const confirmPassword = confirmPasswordInput.value.trim();

    passwordStatus.textContent = "";
    passwordStatus.className = "password-status-message";

    if (!oldPassword || !newPassword || !confirmPassword) {
        submitPasswordButton.disabled = true;
        return;
    }

    if (newPassword.length < 5) {
        passwordStatus.textContent =
        "Password must be at least 5 characters.";
        passwordStatus.classList.add("password-error");
        submitPasswordButton.disabled = true;
        return;
    }

    if (newPassword !== confirmPassword) {
        passwordStatus.textContent = "Passwords do not match.";
        passwordStatus.classList.add("password-error");
        submitPasswordButton.disabled = true;
        return;
    }

    submitPasswordButton.disabled = false;
}



oldPasswordInput.addEventListener("input", validatePasswordForm);
newPasswordInput.addEventListener("input", validatePasswordForm);
confirmPasswordInput.addEventListener("input", validatePasswordForm);

/* ============================= */
/* SUBMIT */
/* ============================= */

changePasswordForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const token = getAcessToken()

    const formData = new FormData(changePasswordForm)

    const data = {
      old_password: formData.get("old-password"),
      new_password: formData.get("confirm-password")
    }

    try {

      const response = await fetch('/api/users/me/change_password', {
      method: "PATCH",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })

      if (!response.ok) {
        const result = await response.json()
        console.log(result)
        passwordStatus.textContent = result.detail;
        passwordStatus.className = "password-status-message password-error";
        return
      }

      const result = await response.json()
      
      // passwordStatus.textContent = "Updating password...";
      passwordStatus.textContent = result.message;
      passwordStatus.className = "password-status-message password-success";

      oldPasswordInput.value = ""
      newPasswordInput.value = ""
      confirmPasswordInput.value = ""

    } catch(error) {
      console.log(error)
      console.log("Something went wrong")
    }
    // passwordStatus.textContent = "Updating password...";
    // passwordStatus.className = "password-status-message password-success";
  });

}

init()



