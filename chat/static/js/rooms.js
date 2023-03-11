
const buttons = document.querySelectorAll('.edit-room')
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
    // get the form relate to its id
    const editForm = document.querySelector(`#edit-form-${resetBtn.id}`)
    // hid it
    hideEditForm(editForm)
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
    event.preventDefault(); 

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


// btnEditRoom.addEventListener('click', function updateObject(buttonId, updatedValue) {
//     // Retrieve the existing object from the server
//     fetch(`http://127.0.0.1:8000/chat/api-auth/room/${buttonId}/`)
//       .then(response => response.json())
//       .then(object => {
//         // Modify the necessary attribute value
//         object.name = prompt()
//         // object.name = updatedValue;
//         // Send the updated object back to the server
//         fetch(`http://127.0.0.1:8000/chat/api-auth/room/${buttonId}/`, {
//           method: 'PUT',
//           headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrf_token(),
//           },
//           body: JSON.stringify(object),
//         })
//         .then(response => {
//           if (response.ok) {
//             console.log('Object updated successfully');
//           } else {
//             console.log('Object update failed');
//           }
//         })
//         .catch(error => console.log('Error:', error));
//       })
//       .catch(error => console.log('Error:', error));
// })

//Create room button handler

btnCreateRoom.addEventListener('click', () => {
  console.log('button.id:', button.id)
  // get the form relate to its id
  const editForm = document.querySelector(`#edit-form-${button.id}`)
  // show it
  showEditForm(editForm)
  // submit button handler
  editForm.addEventListener('submit', function(event) {
  // stop submitting the form
  event.preventDefault(); 

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
      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrf_token(),
        },
        body: JSON.stringify(object),
        }
      fetch(`http://127.0.0.1:8000/chat/api-auth/room/${button.id}/`, options)
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
    hideEditForm(editForm); 
  })
})




// btnCreateRoom.addEventListener('click', () => {



//   })

