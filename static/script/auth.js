
let currentUser = null
let fetchPromise = null 


export async function getCurrentUser() {

  if (currentUser) {
    return currentUser
  }

  if (fetchPromise) {
    return fetchPromise
  }


  const token = getAcessToken()

  fetchPromise = (async () => {
    
    try {

      const response = await fetch("/api/users/me", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      if (response.ok) {

        const user = await response.json()
        currentUser = user;
        return user

      } else {

        removeAcessToken()
        return null
      }

    } catch(error) {

      console.log("Please check your network")
      return null

    } finally {
      fetchPromise = null
    }

  })();

  return fetchPromise
}



export function saveAcessToken(token) {
  localStorage.setItem("access_token", token)
}

export function getAcessToken() {
  return localStorage.getItem("access_token")
}

export function removeAcessToken() {
  localStorage.removeItem("access_token")
}