
const changeAvaBtn = document.querySelector('.change-ava')
const changeName = document.querySelector('.change-name')
const userProfileId = document.getElementById(`userProfile-id`).textContent 
const apiLink = 'http://127.0.0.1:8000/chat/api-auth/userProfile/'
const apiAvatar = 'http://127.0.0.1:8000/media/avatars/'
const fileInput = document.querySelector('#file-input')
const cancelBtn = document.querySelector('.cancel')
const cancelNameBtn = document.querySelector('.cancel-name')
const nameInput = document.querySelector('#edit-name')

console.log('userProfileId:', userProfileId)

fileInput.style.display = 'none'

// csrf_token function
function csrf_token() {
    var csrf_token = null;
    var cookies = document.cookie.split(';')
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim()
      if (cookie.substring(0, 'csrftoken'.length + 1) == ('csrftoken' + '=')) {
        csrf_token = decodeURIComponent(cookie.substring('csrftoken'.length + 1))
        break
      }
    }
    return csrf_token
  }

  cancelBtn.addEventListener('click', () => {
    fileInput.style.display = 'none'
  })

  cancelNameBtn.addEventListener('click', () => {
    nameInput.style.display = 'none'
  })

// change name button handler
  changeName.addEventListener('click', () => {

    nameInput.style.display = 'block'

    const newNameInput = document.querySelector(`#new-name`)
    nameInput.addEventListener('submit', function(event) {
      // stop submitting the form
      event.preventDefault()
      const newName = newNameInput.value
      console.log(newName)

      // API handler
      // get the object from the server 
      fetch(`${apiLink}${userProfileId}/`)
      .then(response => response.json())
      .then(object => {

      // get user id
      const userId = object.user.split('/')
      console.log('userId:', userId[6])

      fetch(`http://127.0.0.1:8000/chat/api-auth/user/${userId[6]}/`)
      .then(response => response.json())
      .then(object => {

        object.username = newName

        fetch(`http://127.0.0.1:8000/chat/api-auth/user/${userId[6]}/`, {
        method: 'PUT',
        headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token(),
        },
        body: JSON.stringify(object),
      })
        .then(response => {
        if (response.ok) {
          console.log('Object updated successfully')
          window.location.href = `/chat/user/${userId[6]}`
        } else {
          console.log('Object update failed')
        }
      })
      .catch(error => console.log('Error:', error))
       
        })
      })
    })
  })

// change ava button handler
  changeAvaBtn.addEventListener('click', () => {

    fileInput.style.display = 'block'
    
    fileInput.addEventListener('change', function(event) {
    event.preventDefault()
   
    const fileName = event.target.value.split('\\').pop() // get a file name
    console.log('fileName', fileName) 

    })  
  })


