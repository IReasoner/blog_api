import {saveAcessToken} from "../script/auth.js";

const loginForm = document.querySelector('.js-login-form');
const loginEmail = document.querySelector('.js-login-email');
const loginPassword = document.querySelector('.js-login-password');
const loginMessage = document.querySelector('.js-login-message');

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const loginData = {
    email: loginEmail.value,
    password: loginPassword.value
  };

  

  // const formData = new URLSearchParams()
  const formData = new FormData();
  formData.append("username", loginData.email)
  formData.append("password", loginData.password)

  try {

  const response = await fetch('/api/users/login', {
    method: 'POST',
    // headers: {
    //   'Content-Type': 'application/x-www-form-urlencoded'
    // },
    body: formData
  });

    if (response.ok) {

    const data = await response.json()
    saveAcessToken(data.access_token)

    setTimeout(() => {
      location.href = "/";
    }, 1000)
    
    loginMessage.textContent = 'Login successful';

    } else {
      const error = await response.json();
      loginMessage.textContent = error.detail;
    }

    } catch(error) {
     loginMessage.textContent = "Something Failed";
  }
});

