 // File: script.js


 function getCookie(name) {
  const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return cookieValue ? cookieValue.pop() : '';
}


// -------------------- FUNCTIONS --------------------

// FUNC - 1: PROFILE DETAIL - BIO - EDIT-PENCIL
function initBioEditing() {


  const editPencilBio = document.querySelector('.edit-pencil-bio');
  // EVENT: EDIT-PENCIL - BIO
  if (editPencilBio) {
    editPencilBio.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      closeOpenDropdownAndDisableBio();
  
      const bioElement = document.querySelector("[data-field-name='bio']");
      bioElement.focus();
    });
  
  
    
    
  // EVENT: 'contenteditable' 
  const bioElement = document.querySelector("[data-field-name='bio']");
  if (bioElement) {
  bioElement.addEventListener('blur', () => {
  const newValue = bioElement.textContent;
  sendUpdatedValueToServer('bio', newValue);
  });
  }
  }
}
// FUNC - 2: PROFILE DETAIL - CLOSE DROPDOWN
function closeOpenDropdownAndDisableBio() {
document.querySelectorAll(".dropdown-menu").forEach((dropdown) => {
  dropdown.style.display = "none";
});

const bioElement = document.querySelector("[data-field-name='bio']");
if (bioElement && bioElement.getAttribute("contenteditable") === "true") {
  bioElement.blur();
}
}
// FUNC - 3: PROFILE DETAILS - UPDATE
function updateProfileField(fieldElement, newValue, newTextContent) {
fieldElement.setAttribute("data-value", newValue);
fieldElement.textContent = newTextContent;
const fieldName = fieldElement.getAttribute("data-field-name");
sendUpdatedValueToServer(fieldName, newValue);
}
// FUNC - 4: PROFILE DETAILS - SAVE DETAIL
function sendUpdatedValueToServer(fieldName, newValue) {
  const user_id = document.querySelector("[data-user-id]").getAttribute("data-user-id");
  const data = { fieldName: fieldName, value: newValue };

  fetch(`/user_profile_field_update/${user_id}/`, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
  .then((response) => {
    // Handle server-side errors
    if (!response.ok) {
      throw new Error("Network response was not ok. Status: " + response.status);
    }
    return response.json();
  })
  .then((data) => {
    console.log("Field update success:", data);
  })
  .catch((error) => {
    console.error("Field update error:", error);
  });
}
// FUNC - 5: PROFILE DETAILS - INITIALIZER
function initProfileDetailsEventListeners() {
  // EVENT 1: PROFILE DETAILS - EDIT BIO
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".edit-pencil-container")) {
      closeOpenDropdownAndDisableBio();
    }
  });

  // ... (other event listeners) ...
}

// FUNC - 6: Handle user search
function handleUserSearch(query) {
  fetch('/user_search/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({
      search_query: query,
    }),
  })
    .then(response => response.json())
    .then(data => {
      const users = data.users;
      handleUserSearchResults(users);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// FUNC - 7: Handle user search results
function handleUserSearchResults(users) {
  const searchResults = document.getElementById('search-results');
  searchResults.innerHTML = '';

  let foundMatch = false;

  for (const user of users) {
    const link = document.createElement('a');
    link.href = '/user_profile/' + user.username + '/';
    link.textContent = user.first_name + ' ' + user.last_name;
    const li = document.createElement('li');
    li.appendChild(link);
    searchResults.appendChild(li);

    foundMatch = true;
  }

  if (!foundMatch) {
    searchResults.innerHTML = '<p>No users found</p>';
  }
}

// FUNC - 8: UPDATE IMAGE PREVIEW
function updateImagePreview(event) {
  const fileInput = event.target;
  const file = fileInput.files[0];
  const imagePreview = document.getElementById('image-preview');

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
    };
    reader.readAsDataURL(file);
  } else {
    imagePreview.src = '';
  }
}

// -------------------- EVENT-LISTENERS --------------------
// EVENT 1: PROFILE DETAILS - EDIT BIO
document.addEventListener("click", (event) => {
  if (!event.target.closest(".edit-pencil-container")) {
  closeOpenDropdownAndDisableBio();
  }
});
// EVENT 2: PROFILE DETAILS
document.querySelectorAll("[data-field-name]").forEach((fieldElement) => {
fieldElement.addEventListener("change", () => {
const fieldName = fieldElement.getAttribute("data-field-name");
const newValue = fieldElement.getAttribute("data-value");
sendUpdatedValueToServer(fieldName, newValue);
});
});
// EVENT 3: DROPDOWN MENU
document.querySelectorAll(".dropdown-menu a").forEach(function (menuItem) {
menuItem.addEventListener("click", function (event) {
event.preventDefault();

const dropdownMenu = event.target.parentElement;
const fieldName = dropdownMenu.getAttribute("data-field-name");
const fieldElement = document.querySelector(`[data-field-name="${fieldName}"]`);
const selectedValue = event.target.getAttribute("data-value");

updateProfileField(fieldElement, selectedValue, event.target.textContent);
dropdownMenu.style.display = "none";
});
});
// EVENT 4: EDIT-PENCIL - DROPDOWN MENU
document.querySelectorAll(".edit-pencil").forEach(function (pencil) {
pencil.addEventListener("click", function (event) {
event.preventDefault();
event.stopPropagation();

closeOpenDropdownAndDisableBio();

const dropdownMenu = pencil.nextElementSibling;
if (dropdownMenu.style.display === "none" || dropdownMenu.style.display === "") {
  dropdownMenu.style.display = "block";
} else {
  dropdownMenu.style.display = "none";
}
});
});




// EVENT 7: FILE INPUT CHANGE
const fileInput = document.getElementById('file-input');
if (fileInput) {
  fileInput.addEventListener('change', updateImagePreview);
}



// EVENT: DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  initBioEditing();

  const postLikeForm = document.getElementById('post-like-form');
  const likeButton = document.getElementById('post-like-button');
  const likeCount = document.getElementById('post-like-count');

 // Check if postLikeForm, likeButton, and likeCount exist before adding the event listener
 if (postLikeForm && likeButton && likeCount) {
  postLikeForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const postId = likeButton.getAttribute('data-post-id');
    const url = `/post_details/toggle-like/${postId}/`;

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
    })
      .then(response => response.json())
      .then(data => {
        likeButton.classList.toggle('liked', data.post_like_status);
        likeButton.textContent = data.post_like_status ? 'Unlike' : 'Like';
        likeCount.textContent = data.like_count;
      })
      .catch(error => {
        console.error('Error:', error);
      });
  });
}
// Call the initializer for the profile details event listeners
initProfileDetailsEventListeners();

   // Step 2: Retrieve element references
   const searchInput = document.getElementById('search-input');
   const searchResults = document.getElementById('search-results');
 
   // Step 3: Check if elements exist
   if (searchInput && searchResults) {
     // Step 4: Attach event listeners
 
     // Event listener function for the 'input' event
     function handleSearchInput(event) {
       const query = event.target.value.trim(); // Trim any leading or trailing whitespace
       if (query.length === 0) {
         handleUserSearchResults([]);
       } else {
         handleUserSearch(query);
       }
     }
 
     // Event listener function for the 'change' event
     function handleSearchResults(event) {
       const selectedUser = event.target.value;
       if (selectedUser) {
         window.location.href = `/user_profile/${selectedUser}/`;
       }
     }
 
     // Attach event listeners
     searchInput.addEventListener('input', handleSearchInput);
     searchResults.addEventListener('change', handleSearchResults);
   }
 });
  


