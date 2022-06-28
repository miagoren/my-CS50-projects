let page = 1;
let pages = undefined;

window.onpopstate = function(event) {
  try {
    page = event.state.page;
  } catch (e) {
    console.error(e);
  }
  load_page();
}

document.addEventListener('DOMContentLoaded', () => {
  load_page();
  history.pushState({page: page}, "", page); // Push state to history
});

// Load the opportunities for this page
function load_page() {
  fetch(`${get_url('helpers')}?page=${page}`)
  .then(response => response.json())
  .then(result => {
    const helpers = result['helpers'];
    pages = result['pages'];
    document.querySelector('#helpers').innerHTML = '';

    helpers.forEach(helper => {
      // Make helper element
      let badge = create_element('div', {'className': 'col-1 display-4'});
      badge.append(create_element('p', {'className': 'badge badge-info', 'innerHTML': helper.helped}));

      let head = create_element('div', {'className': 'd-flex justify-content-between'});
      head.append(create_element('h5', {'innerHTML': helper.username}));
      head.append(create_element('small', {'innerHTML': `Last seen: ${helper.last_seen}`}));

      let info = create_element('div', {'className': 'col'});
      info.append(head);
      info.append(create_element('p', {'innerHTML': `From ${helper.location}`}));

      let box = create_element('a', {'className': 'list-group-item list-group-item-action', 'href': get_url('user', helper.id)});
      box.append(create_element('div', {'className': 'row no-gutters'}));
      box.firstElementChild.append(badge);
      box.firstElementChild.append(info);

      document.querySelector('#helpers').append(box);
      make_nav();
    });
  })
  .catch(error => {
    page = 1;
    load_page();
    history.pushState({page: page}, "", page); // Push state to history
  });
}

// Make the pagination bar
function make_nav() {
  if (pages == 1) {
    return;
  }
  const navigator = create_element('ul', {'className': 'pagination justify-content-center'});

  if (page > 1) {
    // Create previous button
    const icon = document.createElement('li');
    icon.className = "page-item";

    const link = create_element('span', {'className': 'page-link', 'innerHTML': 'Previous', 'style': 'cursor: pointer'});
    link.onclick = function() {
      page --;
      history.pushState({page: page}, "", page); // Push state to history
      load_page(page);
      document.querySelector('.box-style').scrollIntoView();
    };

    icon.append(link);
    navigator.append(icon);
  }

  if (page < pages) {
    // Create next button
    const icon = document.createElement('li');
    icon.className = "page-item";

    const link = create_element('span', {'className': 'page-link', 'innerHTML': 'Next', 'style': 'cursor: pointer'});
    link.onclick = function() {
      page ++;
      history.pushState({page: page}, "", page); // Push state to history
      load_page(page);
      document.querySelector('.box-style').scrollIntoView();
    };

    icon.append(link);
    navigator.append(icon);
  }

  document.querySelector('#pagination').innerHTML = '';
  document.querySelector('#pagination').append(navigator);
}

// Create an html element with paramethers from info
function create_element(type, info={}) {
  const element = document.createElement(type);

  Object.keys(info).forEach((key) => {
    element[key] = info[key];
  });

  return element;
}
