let currentUser = null;

async function loadingUser() {
    currentUser = await getCurrentUser();
}

async function init() {
    await loadingUser();

    // everything below can safely use currentUser
    showProfile();
    loadPosts();
    updateNavbar();
}

function showProfile() {
    console.log(currentUser.username);
}

init();