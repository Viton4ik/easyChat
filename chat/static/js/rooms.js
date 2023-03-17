
const buttons = document.querySelectorAll('.edit-room')
const btnsDeleteRoom = document.querySelectorAll('.delete-room')
const btnsJoinRoom = document.querySelectorAll('.enter-room')
const btnCreateRoom = document.querySelector('.create-room')
const resetBtns = document.querySelectorAll('.cancel')

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

// hide a form
function hideEditForm(editForm) {
  editForm.style.display = 'none'
}

// show a form
function showEditForm(editForm) {
  editForm.style.display = 'block'
}

// reset button handler
resetBtns.forEach(resetBtn => {
  resetBtn.addEventListener('click', () => {
    if (resetBtn.id) {
      // if button is editRoom
      const editForm = document.querySelector(`#edit-form-${resetBtn.id}`)
      hideEditForm(editForm)
    } else {
      // if button is createRoom
      const createForm = document.querySelector(`#create-form`)
      hideEditForm(createForm)
    }
  })
})

//edit room buttons handler
buttons.forEach(button => {
  button.addEventListener('click', () => {
    console.log('button.id:', button.id)
    // get the form relate to its id
    const editForm = document.querySelector(`#edit-form-${button.id}`)
    // show it
    showEditForm(editForm)
    // submit button handler
    editForm.addEventListener('submit', function(event) {
    // stop submitting the form
    event.preventDefault()

    // get form's tags
    const roomNameDisplay = document.querySelector(`#room-name-display-${button.id}`)
    const newRoomNameInput = document.querySelector(`#new-room-name-${button.id}`)
    //set a new name for the specific room
    const newRoomName = newRoomNameInput.value; 

    // API handler
    // retrieve the existing object from the server
    fetch(`http://127.0.0.1:8000/chat/api-auth/room/${button.id}/`)
      .then(response => response.json())
      .then(object => {
        // modify the necessary attribute value
        // object.name = prompt(`new a name for the room '${object.name}'`)
        object.name = newRoomName
        // refresh the name of the room on the page
        roomNameDisplay.textContent = `'${newRoomName}'`
        // send the updated object back to the server
        fetch(`http://127.0.0.1:8000/chat/api-auth/room/${button.id}/`, {
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
            // refresh the page
            // location.reload()
          } else {
            console.log('Object update failed')
          }
        })
        .catch(error => console.log('Error:', error))
      })
      .catch(error => console.log('Error:', error))
      // hide the form
      hideEditForm(editForm)
  })
})
})

const userId = document.getElementById(`user-id`) // get user id tag 
const currentUser = `http://127.0.0.1:8000/chat/api-auth/user/${userId.textContent}/`
console.log('userId:', userId)
console.log('currentUser:', currentUser)

//Join room button handler
btnsJoinRoom.forEach(button => {
  button.addEventListener('click', () => {
    console.log('button.id:', button.id)

    // API handler
    // retrieve the existing object from the server
    fetch(`http://127.0.0.1:8000/chat/api-auth/room/${button.id}/`)
      .then(response => response.json())
      .then(object => {
        // modify the necessary attribute value
        object.users.push(currentUser)
        // send the updated object back to the server
        fetch(`http://127.0.0.1:8000/chat/api-auth/room/${button.id}/`, {
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
            // go to the related page of the room
            window.location.href = `http://127.0.0.1:8000/chat/rooms/${button.id}`
          } else {
            console.log('Object update failed')
          }
        })
        .catch(error => console.log('Error:', error))
      })
      .catch(error => console.log('Error:', error))
})
})

const roomIds = document.querySelectorAll('.roomId')
// is user in a room function
roomIds.forEach(roomId => {
  fetch(`http://127.0.0.1:8000/chat/api-auth/room/${roomId.textContent}/`)
  .then((response) => {
    const result = response.json()
    return result;
  })
  .then((data) => {
    console.log('data',data)
    if (data.users.includes(currentUser)) {
      console.log('user in')
      const participant = document.querySelector(`#participant-${roomId.textContent}`)
      showEditForm(participant)
    } else {
      console.log('user out')
      const participant = document.querySelector(`#no-participant-${roomId.textContent}`)
      showEditForm(participant)
    }
  })
  .catch(() => { console.log('error') })
})

//Delete room button handler
btnsDeleteRoom.forEach(button => {
  button.addEventListener('click', () => {
      console.log('button.id:', button.id)
      // get the form relate to its id
      const confirmationForm = document.querySelector(`#confirmation-form-${button.id}`)
      // show it
      showEditForm(confirmationForm)
      const confirmButton = document.querySelector(`#confirm-button-${button.id}`)
      const cancelButton = document.querySelector(`#cancel-button-${button.id}`)

      confirmButton.addEventListener('click', function() {
          // API handler
          fetch(`http://127.0.0.1:8000/chat/api/deleteChat/${button.id}`)
          .then(response => {
            if (response.ok) {
              console.log('Object deleted successfully')
              // refresh the page
              location.reload()
            } else {
              console.log('Object deleting failed')
            }
          })
          .catch(error => console.log('Error:', error))
      })
      cancelButton.addEventListener('click', function() {
        hideEditForm(confirmationForm)
        })
      })
    })

const createForm = document.querySelector(`#create-form`)
const newRoomNameInput = document.querySelector(`#new-room-name`)


// console.log(userId.textContent) // get user id

//Create room button handler
btnCreateRoom.addEventListener('click', () => {
  // show the create form
  showEditForm(createForm)
  // submit button handler
  createForm.addEventListener('submit', function(event) {
  // stop submitting the form
  event.preventDefault()
  //set a new name for new room
  const newRoomName = newRoomNameInput.value
  console.log(newRoomName)

  // API handler
  const object = {
    name: newRoomName, 
    users: [currentUser]
    // users: [`http://127.0.0.1:8000/chat/api-auth/user/${userId.textContent}/`]
  }
  console.log(JSON.stringify(object))
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token(),
    },
    body: JSON.stringify(object),
    }
  fetch(`http://127.0.0.1:8000/chat/api-auth/room/`, options)
  .then(response => {
    if (response.ok) {
      console.log('Object updated successfully')
      // refresh the page
      location.reload()
    } else {
      console.log('Object update failed')
    }
  })
  .catch(error => console.log('Error:', error))
  // hide the form
  hideEditForm(createForm)
})
})

