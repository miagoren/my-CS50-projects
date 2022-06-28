let conversation = 'unset';
if (go_to != '') {
  conversation = parseInt(go_to);
}

window.onpopstate = function(event) {
  try {
    conversation = event.state.conversation;
  } catch (e) {
    console.error(e);
  }
  get_conversations();
}

document.addEventListener('DOMContentLoaded', () => {
  get_conversations();

  document.getElementById('new-message').onsubmit = function() {
    make_message(this.firstElementChild.value);
    return false;
  };

});

// Get this user's conversations
function get_conversations() {
  fetch(`${get_url('messaging')}?action=get_conversations`)
  .then(response => response.json())
  .then(result => {
    conversations = result.conversations;
    document.getElementById('convo-box').innerHTML = '';
    document.getElementById('convo-box').append(create_element('a', {'className': 'list-group-item list-group-item-action font-weight-bold', 'innerHTML': 'Create a new conversation'}));
    document.querySelector('#convo-box').firstElementChild.onclick = make_conversation;

    if (conversations.length === 0) {
      conversation = 0;
    }

    if (conversation === 0) {
      document.querySelector('#convo-box').firstElementChild.classList.add('list-group-item-info');
      document.getElementById('messages').style.display = 'none';
      document.getElementById('new-conversation').style.display = 'initial';
    } else if (conversation === 'unset') {
      conversation = conversations[0].id;
      document.getElementById('new-conversation').style.display = 'none';
    } else {
      document.getElementById('new-conversation').style.display = 'none';
    }

    conversations.forEach((convo) => {
      const convo_element = create_element('a', {'className': 'list-group-item list-group-item-action', 'innerHTML': convo.subject});
      convo_element.dataset.id = convo.id;
      if (convo.id === conversation) {
        convo_element.classList.add('list-group-item-info');
      }
      convo_element.addEventListener('click', function() {
        document.getElementById('messages').style.display = 'initial';
        document.getElementById('new-conversation').style.display = 'none';
        conversation = this.dataset.id;
        this.parentElement.getElementsByClassName('list-group-item-info')[0].classList.remove('list-group-item-info');
        this.classList.add('list-group-item-info');
        get_messages();
        history.pushState({conversation: conversation}, "", conversation); // Push state to history
      });
      document.getElementById('convo-box').append(convo_element);
    });

    if (conversation != 0) {
      get_messages();
    }
    history.pushState({conversation: conversation}, "", conversation); // Push state to history
  })
  .catch(e => console.error(e));
}

// Create a new conversation
function make_conversation() {
  conversation = 0;
  this.parentElement.getElementsByClassName('list-group-item-info')[0].classList.remove('list-group-item-info');
  this.classList.add('list-group-item-info');
  document.getElementById('messages').style.display = 'none';
  document.getElementById('new-conversation').style.display = 'initial';
  history.pushState({conversation: conversation}, "", conversation); // Push state to history
}

// Load all messages in current conversation
function get_messages() {
  fetch(`${get_url('messaging')}?action=get_messages&conversation=${conversation}`)
  .then(response => response.json())
  .then(result => {
    subject = result.subject;
    recipients = result.recipients;
    messages = result.messages;

    document.getElementById('subject-box').innerHTML = subject;
    document.getElementById('recipient-box').innerHTML = '';
    recipients.forEach((recipient) => {
      var user = create_element('a', {'innerHTML': recipient.username});
      if (recipient.id) {
        user.href = get_url('user', recipient.id);
        document.getElementById('recipient-box').append(user);
        document.getElementById('recipient-box').append(', ');
      } else {
        document.getElementById('recipient-box').append(user);
      }
    });
    const message_box = document.getElementById('message-box');
    message_box.innerHTML = '';

    document.querySelector('button.leave').onclick = function() {
      response = confirm('Are you sure you want to leave this conversation?');
      if (!response) {
        return;
      }
      fetch(`${get_url('messaging')}?action=leave&conversation=${conversation}`)
      .then(response => {
        reload_pages();
      })
      .catch(e => console.error(e))
    };

    messages.forEach((message) => {
      const message_element = create_element('a', {'className': 'list-group-item'});
      if (message.sender.id != user_id && message.sender.id) {
        message_element.append(create_element('strong', {'innerHTML': `${message.sender.username}: `}));
        message_element.classList.add('.my-message');
      }
      message_element.append(create_element('div', {'innerHTML': message.body}));
      message_element.append(create_element('small', {'innerHTML': message.datetime}));

      message_box.append(message_element);
    });

    message_box.scrollBy(0, message_box.scrollHeight - message_box.offsetHeight)
  });
}

// Create a new message
function make_message(text) {
  fetch(get_url('messaging'), {
    method: 'PUT',
    body: JSON.stringify({'text': text, 'conversation': conversation})
  })
  .then(response => {
    document.getElementById('new-message').firstElementChild.value = '';
    get_messages();
  })
  .catch(error => console.error(error));
}

// Create an html element with paramethers from info
function create_element(type, info={}) {
  const element = document.createElement(type);

  Object.keys(info).forEach((key) => {
    element[key] = info[key];
  });

  return element;
}


// Reload after leaving conversation change
function reload_pages() {
  conversation = 'unset';
  get_conversations();
}
