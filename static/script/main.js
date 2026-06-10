import {formatTime} from "../script/utils.js"

const loadButton = document.querySelector(".js-load-more");
const buttonText = document.querySelector(".js-button-text");
const spinner = document.querySelector(".js-loading-spinner");

if (loadButton) {
    loadButton.addEventListener("click", () => {
    loadButton.disabled=true;
    buttonText.textContent = "Loading...";
    spinner.classList.remove("hidden-spinner");
    // Simulate request
    setTimeout(() => {
        loadButton.disabled = false;
        buttonText.textContent= "Load More Posts";
        spinner.classList.add("hidden-spinner");
        loadMorePosts()
    },100);
});

}

const params = new URLSearchParams(
    location.search
)

let currentPage = Number(params.get("page")) || 1
let size = 5

async function loadMorePosts() {

  currentPage ++;

  try {

    const response = await fetch(`/api/posts?page=${currentPage}&size=${size}`)

    if (!response.ok) {
      return
    }

    const data = await response.json()
    loadToPage(data)

    history.pushState(
        {},
        "",
        `/?page=${currentPage}`
    )

    sessionStorage.setItem("home_url", location.href)

    if (!data.has_more) {
      document.querySelector(".js-load-more-container")
      .classList.add("hidden")
    }

  } catch(error) {
    console.log("please check your internet connection")
    console.log(error)
  }

}


function loadToPage(data) {

  let postJoinHTML = ``;
  const posts = data.posts;

  posts.forEach((c) => {

   postJoinHTML += `
   <article class="main-post-card">
            <!-- AUTHOR SECTION -->
            <div class="main-post-author-section">
                <div class="main-post-author-profile">
                    <img
                        class="main-post-author-profile-image"
                         src="${c.to_user.image_url}"
                        alt="author profile"
                    >
                </div>

                <div class="main-post-author-details">
                    <a class="main-post-author-name"
                       href="/user/${c.to_user.id}/posts">
                       ${c.to_user.username}
                    </a>
                    <p class="main-post-date">
                     ${formatTime(c.date_posted)}
                    </p>
                </div>
            </div>

            <!-- POST BODY -->
            <div class="main-post-body">
                <a class="main-post-title-link"
                   href="/post/${c.id}">
                    <h2 class="main-post-title">
                        ${c.title}
                    </h2>
                </a>
                <p class="main-post-content">
                    ${c.content}
                </p>
            </div>

     </article>
   
   `;
  })


  document.querySelector(".js-main-posts-list-container").innerHTML += postJoinHTML;
}