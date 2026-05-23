
import {getCurrentUser, getAcessToken} from "../script/auth.js"


// ALL DEFINE ELEMENT FOR CREATE POST
const form = document.querySelector(".postForm");
const homeWrapper = document.querySelector(".js-over-all-wrapper");
const containeredit = document.querySelector(".js-edit-container");
const newPostBtn = document.querySelector(".js-create-new-post");
const loggedInButton = document.querySelector(".js-login-button");
const registrationButton = document.querySelector(".js-register-button");
const userDetail = document.querySelector(".js-user-container");
const toggle_div = document.querySelector(".js-all-body-pages")


// GENERAL CODE
let showEdit = false

function toggle_edit(element) {
    if (element.classList.contains("hide")) {
      element.classList.remove("hide")
      element.classList.add("show-flex")
    } else {
      element.classList.remove("show-flex")
      element.classList.add("hide")
    } 
}

// GENERAL ENDS

// CODE FOR CREATING NEW POST

form.addEventListener("submit", async (event) => {
  event.preventDefault();


  const formData = new FormData(form)
  const dataObj = Object.fromEntries(formData); 

    const token = getAcessToken()

    await fetch("http://127.0.0.1:8000/api/posts", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify(dataObj)
  });

  toggle_edit(homeWrapper)
  form.reset();
  location.reload()
})


document.querySelector(".js-create-new-post").addEventListener("click", () => {
  toggle_edit(homeWrapper)
})

document.querySelector(".js-cancel-home").addEventListener("click", () => {
  toggle_edit(homeWrapper)
})


// ALL DEFINE ELEMENT FOR EDIT POST
const formedit = document.querySelector(".editPostForm");

if (formedit) {

const editWrapper = document.querySelector(".js-all-wrapper-edit");

let currentID = null



// EDIT POST LOGIC
// THE BEGIN OF ADVANCE STOPTING OF BAD RUN TWICE AND THREE TIMES

function editPost(id, title, content) {

  toggle_edit(editWrapper)
  showEdit = true
  
  currentID = id;

  containeredit.querySelector(".js-title").value = title;
  containeredit.querySelector(".js-content").value = content;

 }

 // THIS SHOULD ONLY DEFINE ONE

 formedit.addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(formedit)
      const dataObj = Object.fromEntries(formData); 

        await fetch(`http://127.0.0.1:8000/api/posts/${currentID}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(dataObj)
      })


      toggle_edit(editWrapper)
      formedit.reset();
      location.reload()
  })

  // END OF THE LOGIC
  document.querySelector(".js-cancel-edit").addEventListener("click", () => {
    toggle_edit(editWrapper)
  })

  document.querySelector(".js-edit-button").addEventListener("click", () => {
    
    const blogContainer = document.querySelector(".blog_container_post")
    const title = blogContainer.querySelector(".js-title-f").innerHTML;
    const content = blogContainer.querySelector(".js-content-f").innerHTML;
    const postID = blogContainer.dataset.postId;
    
    editPost(postID, title, content)
  })

  document.querySelector(".js-delete-button").addEventListener("click", async () => {
    const blogContainer = document.querySelector(".blog_container_post")
    const postID = blogContainer.dataset.postId;

     await fetch(`http://127.0.0.1:8000/api/posts/${postID}`, {
      method: "DELETE"
      })

      location.href = "/"
  })

  }


function checkIfUserLogin() {

  const token = localStorage.getItem("access_token")

  if (!token) {

    // HIDING
    newPostBtn.classList.add("hide")
    newPostBtn.classList.remove("show-initial")

    userDetail.classList.add("hide")
    userDetail.classList.remove("show-initial")

    // SHOWING
    loggedInButton.classList.remove("hide")
    loggedInButton.classList.add("show-initial")

    registrationButton.classList.remove("hide")
    registrationButton.classList.add("show-initial")

    if (toggle_div) {
      toggle_div.style.display = "none"
    }

   

  } else {
    // SHOWING
    newPostBtn.classList.remove("hide")
    newPostBtn.classList.add("show-initial")

    userDetail.classList.remove("hide")
    userDetail.classList.add("show-initial")

    // HIDING
    loggedInButton.classList.add("hide")
    loggedInButton.classList.remove("show-initial")

    registrationButton.classList.add("hide")
    registrationButton.classList.remove("show-initial")
   
    if (toggle_div) {
      toggle_div.style.display = "initial"
    }
    
    loadUser()
  }
}

checkIfUserLogin()

async function loadUser() {
  const user = await getCurrentUser()

  if (!user) {
    console.log("no user")
    return 
  }

  document.querySelector(".js-user-img").src = user.image_url
  document.querySelector(".js-user-email").innerHTML = user.email
  document.querySelector(".js-user-username").innerHTML = user.username

}
