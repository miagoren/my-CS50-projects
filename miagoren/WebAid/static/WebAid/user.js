document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.edit-show').forEach((item) => {
    item.style.display = 'none';
  });

  // Edit profile page
  var edit_el = document.getElementById('edit');
  edit_el && edit_el.addEventListener('click', function() {
    if (this.innerHTML === 'Edit profile info') {
      // Edit page
      document.querySelectorAll('.edit-show').forEach((item) => {
        item.style.display = 'initial';
      });
      document.querySelectorAll('.edit-hide').forEach((item) => {
        item.style.display = 'none';
      });
      this.innerHTML = 'Save changes';
    } else {
      var location = document.getElementsByName('location')[0].value;
      var skills = document.getElementsByName('skills')[0].value;

      fetch(get_url('user', user_id), {
        method: 'PUT',
        body: JSON.stringify({'location': location, 'skills': skills}),
      })
      .then(data => {
        window.location.reload(true);
      });
    }
  });

  // Message user
  var message_el = document.getElementById('message');
  message_el && message_el.addEventListener('click', function() {
    document.getElementById('message-form').submit();
  });
});
