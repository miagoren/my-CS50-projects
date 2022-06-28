let page = 1;
let pages = undefined;

let filters = {
  'categories': [],
  'location': '',
  'creation_time': ''
};
if (localStorage.defaultSearch) {
  filters = JSON.parse(localStorage.defaultSearch);
}
if (pre_category) {
  filters.categories= [pre_category];
}

window.onpopstate = function(event) {
  try {
    page = event.state.page;
  } catch (e) {
    console.error(e);
  }
  make_filters();
  load_page();
}

document.addEventListener('DOMContentLoaded', () => {
  make_filters();
  load_page();
  history.pushState({page: page}, "", page); // Push state to history
});

// Make the filter bar
function make_filters() {
  // Categories filter
  document.getElementById('categories').addEventListener('blur', function add_category() {
    if (this.value.trim() === '') {
      // Clear input field
      this.value = '';
    }
  });
  document.getElementById('categories').addEventListener('keyup', function(event) {
    if (event.keyCode === 13) {
      let category = this.value.trim();

      if (filters.categories.includes(category)) {
        // Clear input field
        this.value = '';
        return;
      }

      if (category != '') {
        // Add category to list and badge to DOM
        filters.categories.push(category);
        document.getElementById('category-badges').append(make_badge(category));
        reload_pages();
      }

      // Clear input field
      this.value = '';
    }
  });

  // Category badges
  if (filters.categories != '') {
    filters.categories.forEach((category) => {
      document.getElementById('category-badges').append(make_badge(category));
    });
  }

  // Location filter
  if (filters.location) {
    document.getElementById('location').value = filters.location;
  }
  document.getElementById('location').addEventListener('change', function() {
    filters.location = this.value;
    reload_pages();
  });

  // Creation time filter
  if (filters.creation_time) {
    document.getElementById('creation_time').value = filters.creation_time;
  }
  document.getElementById('creation_time').onchange = function() {
    filters.creation_time = this.value;
    reload_pages();
  }

  // Default filters button
  document.querySelector('#filter-box').querySelector('button').onclick = function() {
    localStorage.defaultSearch = JSON.stringify(filters);
  }
}

// Load the opportunities for this page
function load_page() {
  let query = `/opportunities/?page=${page}`;
  if (filters.categories != '') {
    query = query.concat(`&categories=${filters.categories.toString()}`)
  }
  if (filters.location) {
    query = query.concat(`&location=${filters.location}`);
  }
  if (filters.creation_time) {
    query = query.concat(`&creation_time=${filters.creation_time}`);
  }
  fetch(query)
  .then(response => response.json())
  .then(result => {
    const opportunities = result['opportunities'];
    pages = result['pages'];
    if (opportunities.length == 0) {
      document.querySelector('#no-opportunities').style.display = 'initial';
      document.querySelector('#opportunities').innerHTML = '';
      return;
    }
    document.querySelector('#no-opportunities').style.display = 'none';
    document.querySelector('#opportunities').innerHTML = '';
    opportunities.forEach(opportunity => {
      // Make opportunity box
      let box = create_element('a', {'className': 'list-group-item list-group-item-action opportunity', 'href': `../opportunity/${opportunity.id}`});

      let head = create_element('div', {'className': 'd-flex justify-content-between'});
      head.append(create_element('h5', {'innerHTML': opportunity.title}));
      head.append(create_element('small', {'innerHTML': opportunity.creation_time}));

      box.append(head);
      box.append(create_element('p', {'innerHTML': opportunity.description}));
      box.append(create_element('small', {'innerHTML': opportunity.location}));

      document.querySelector('#opportunities').append(box);
      make_nav();
    });
  })
  .catch(error => {
    page = 1;
    load_page();
    make_nav();
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

// Create a category badge
function make_badge(name) {
  const badge = create_element('li', {'className': 'badge badge-pill badge-info', 'innerHTML': `${name} `});
  const close = create_element('a', {'type': 'button', 'innerHTML': 'x'});
  close.dataset.category = name;
  close.addEventListener('click', function() {
    const category = this.dataset.category;
    let index = filters.categories.indexOf(category);
    filters.categories.splice(index, 1);
    this.parentElement.remove();
    reload_pages();
  })

  badge.append(close);
  return badge;
}

// Reload after filter change
function reload_pages() {
  page = 1;
  load_page();
}
