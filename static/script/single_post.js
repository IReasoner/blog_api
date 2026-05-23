import {getCurrentUser} from "../script/auth.js";

const editDeleteElement = document.querySelector(".js-edit-delete");
const blogContainer = document.querySelector(".js-blog");

const user = await getCurrentUser();

function checkUser() {
  if (!user) {
    return
  }

  const user_id = Number(blogContainer.dataset.userId);

  if (user_id != user.id) {
    editDeleteElement.style.display = "none"
  }

  console.log(user)

}

checkUser()
