
const roomName = JSON.parse(document.getElementById('json-roomname').textContent)
const roomId = JSON.parse(document.getElementById('json-roomId').textContent)
const userName = JSON.parse(document.getElementById('json-username').textContent)
// const createTime = JSON.parse(document.getElementById('date').textContent)
const closeBtn = document.querySelector('.close-btn')
const chatWindow = document.querySelector('.chat-window')

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

// console.log('roomName:',roomName)
// console.log('roomId:',roomId)
// console.log('createTime:',createTime)

// get a WebSocket connection
const chatSocket = new WebSocket(   //'wss://ws.postman-echo.com/raw')
    'ws://'
    // + window.location.host
    + '127.0.0.1:8001'
    // + '/ws/'
    + '/ws/chat/rooms/'
    // + roomName
    + roomId
    + '/'
    // + ''
);

//onMessage finction
chatSocket.onmessage = function(e) {

    // get data from JSON
    const data = JSON.parse(e.data)
    // console.log('data:', data)

    if (data.message) {

        let html = '<div class="chat-messages" id="chat-messages">'
        html += `<p style="font-weight: bold;">${data.username}</p>`
        html += `<p>${data.message}</p>`
        html += `<p class="date" id="date"><em>${data.timestamp.toLocaleString()}</em></p></div>`

        document.querySelector('#chat-body').innerHTML += html

        scrollDownMessage()
    } else {
        alert('The message was empty!')
    }
}
// Enter button handler
document.querySelector('#chat-message-input').focus()
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {
        document.querySelector('#send-btn').click()
    }
}


// Enter button handler
// const inputField = document.getElementById('chat-message-input')
// inputField.addEventListener('keyup', function(event) {
//   if (event.keyCode === 13) { // code for "Enter"
//     event.preventDefault();
//     document.getElementById('send-btn').click(); // call send-btn handler
//   }
// })

chatSocket.onclose = function(e) {
    console.error('The socket closed unexpectedly')
}

// send-btn handler
document.querySelector('#send-btn').onclick = function(e) {
  e.preventDefault()

  const messageInput = document.querySelector('#chat-message-input')
  const message = messageInput.value

  // console.log('message:',message)
  
  chatSocket.send(JSON.stringify({
    'message': message,
    'username': userName,
    'room': roomId,
  }))
  messageInput.value = ''

  return false
}

function scrollDownMessage() {
  let objDiv = document.querySelector('#chat-body')
  objDiv.scrollTop = objDiv.scrollHeight
}

scrollDownMessage()

// "X"-button handler
closeBtn.addEventListener('click', () => {
  chatWindow.style.display = 'none'
})


const forgotRoom = document.querySelector('.forgot-room')
const userId = document.getElementById(`user-id`) // get user id tag 
const chatId = document.getElementById(`room-id`) // get user id tag 
const currentUser = `http://127.0.0.1:8000/chat/api-auth/user/${userId.textContent}/`
const currentRoom = `http://127.0.0.1:8000/chat/api-auth/room/${chatId.textContent}/`

//forgotRoom button handler
forgotRoom.addEventListener('click', () => {
  const confirmationForm = document.querySelector(`#confirmation-form`)
  // show the form
  confirmationForm.style.display = 'block'

  const yesButton = document.querySelector(`#yes-button`)
  const noButton = document.querySelector(`#no-button`)

  yesButton.addEventListener('click', function() {
    // API handler
    // retrieve the existing object from the server
    fetch(currentUser)
    .then(response => response.json())
    .then(object => {
      // modify the necessary attribute value
      const index = object.chats.indexOf(currentRoom) // find an index of the chat in the array
      if (index !== -1) {
        object.chats.splice(index, 1) // delete it from the array
      }
      // send the updated object back to the server
      fetch(currentUser, {
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
          window.location.href = `http://127.0.0.1:8000/chat/rooms`
        } else {
          console.log('Object update failed')
        }
      })
      .catch(error => console.log('Error:', error))
    })
  })
  // hide the form
  noButton.addEventListener('click', () => {
    confirmationForm.style.display = 'none'
    })
})