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


}

init()



