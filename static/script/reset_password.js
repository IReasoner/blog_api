const password = document.querySelector(".js-password");
const confirmPassword = document.querySelector(".js-confirm-password");
const resetButton = document.querySelector(".js-reset-button");
const errorText = document.querySelector(".js-password-error");
const toggleButton = document.querySelector(".js-password-toggle");
const form = document.querySelector(".js-reset-password-form");


const params = new URLSearchParams(location.search)
const token = params.get("token")

console.log(token)

function validatePasswords(){

    const first = password.value;
    const second = confirmPassword.value;

    if (first.length === 0 || second.length === 0) {
        resetButton.disabled = true;
        errorText.textContent = "";
        return;
    }

    if (first !== second) {
        errorText.textContent = "Passwords do not match";
        resetButton.disabled = true;
        return;
    }

    errorText.textContent = "";
    resetButton.disabled = false;

}

password.addEventListener("input", validatePasswords);
confirmPassword.addEventListener("input", validatePasswords);

toggleButton.addEventListener("click", () => {
    password.type = password.type === "password" ? "text" : "password";
});


form.addEventListener("submit", async (e) => {
    e.preventDefault()

    const formData = new FormData(form)

    try {

      const response = await fetch("/api/users/reset_password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: token,
            password: formData.get("confirm-password")
        })
      })

      if (!response.ok) {
        return
      }

      const data = await response.json()
      alert(data.message)

    password.value = ""
    confirmPassword.value = ""

    location.href = "/login"

    } catch(error) {
        console.log(error)
        console.log("Something went wrong")
    }
})