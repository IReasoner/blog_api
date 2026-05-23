
const registerForm = document.querySelector('.js-register-form');
const registerUsername = document.querySelector('.js-register-username');
const registerEmail = document.querySelector('.js-register-email');
const registerPassword = document.querySelector('.js-register-password');
const registerMessage = document.querySelector('.js-register-message');

registerForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const registerData = {
    username: registerUsername.value,
    email: registerEmail.value,
    password: registerPassword.value
  };

  try {

    const response = await fetch('/api/users/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(registerData)
    });


    if (response.ok) {
      
      setTimeout(() => {
        location.href = "/login"
      }, 500)

      registerMessage.textContent = 'Registration successful';

    } else {
      const data = await response.json()
      console.log(data)
      registerMessage.textContent = data.detail

    }

  } catch(error) {
     registerMessage.textContent = error.message;
  }


});