document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.edit-show').forEach((item) => {
    item.style.display = 'none';
  });
  if (!show_resolve && document.getElementById('resolve-form')) {
    document.getElementById('resolve-form').style.display = 'none';
  }

  // Edit this opportunity
  var edit_el = document.getElementById('edit');
  edit_el && edit_el.addEventListener('click', function() {
    if (this.innerHTML === 'Edit this opportunity') {
      // Edit page
      document.querySelectorAll('.edit-show').forEach((item) => {
        item.style.display = 'initial';
      });
      document.querySelectorAll('.edit-hide').forEach((item) => {
        item.style.display = 'none';
      });
      this.innerHTML = 'Save changes';
    } else {
      var title = document.getElementsByName('title')[0].value;
      var location = document.getElementsByName('location')[0].value;
      var categories = document.getElementsByName('categories')[0].value;
      var description = document.getElementsByName('description')[0].value;

      fetch(get_url('opportunity', opportunity_id), {
        method: 'PUT',
        body: JSON.stringify({'title': title, 'location': location, 'categories': categories, 'description': description}),
      })
      .then(data => {
        window.location.reload(true);
      });
    }
  });

  // Resolve this opportunity
  var resolve_el = document.getElementById('resolve');
  resolve_el && resolve_el.addEventListener('click', function() {
    document.getElementById('resolve-form').style.display = 'initial';
  });

  // Volunteer for opportunity
  var volunteer_el = document.getElementById('volunteer');
  volunteer_el && volunteer_el.addEventListener('click', function() {
    document.getElementById('volunteer-form').submit();
  });
});
