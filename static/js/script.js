// File: script.js

function getCookie(name) {
  const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return cookieValue ? cookieValue.pop() : '';
}

// FUNC - 1: PROFILE DETAIL - BIO - EDIT-PENCIL
function handleBioEditing() {
  const editPencilBio = document.querySelector('.edit-pencil-bio');
  
  if (editPencilBio) {
    editPencilBio.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      handleBioDropdownMenu();

      const bioElement = document.querySelector("[data-field-name='bio']");
      bioElement.focus();
    });
  }

  const bioElement = document.querySelector("[data-field-name='bio']");
  if (bioElement) {
    bioElement.addEventListener('blur', () => {
      const profileFieldsNewValue = bioElement.textContent;
      sendUpdatedValueToServer('bio', profileFieldsNewValue);
    });
  }
}

// FUNC - 2: PROFILE DETAIL - CLOSE DROPDOWN
function handleBioDropdownMenu() {
  document.querySelectorAll(".dropdown-menu").forEach((dropdown) => {
    dropdown.style.display = "none";
  });

  const bioElement = document.querySelector("[data-field-name='bio']");
  if (bioElement && bioElement.getAttribute("contenteditable") === "true") {
    bioElement.blur();
  }
}

// FUNC - 3: PROFILE DETAILS - UPDATE
function handleUpdateProfileField(profileFieldElement, profileFieldsNewValue, newTextContent) {
  profileFieldElement.setAttribute("data-value", profileFieldsNewValue);
  profileFieldElement.textContent = newTextContent;
  const profileFieldName = profileFieldElement.getAttribute("data-field-name");
  sendUpdatedValueToServer(profileFieldName, profileFieldsNewValue);
}

// FUNC - 4: PROFILE DETAILS - SAVE DETAIL
function sendUpdatedValueToServer(profileFieldName, profileFieldsNewValue) {
  const user_id = document.querySelector("[data-user-id]").getAttribute("data-user-id");
  const data = { fieldName: profileFieldName, value: profileFieldsNewValue };

  fetch(`/user_profile_field_update/${user_id}/`, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
  .then((response) => {
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
function initProfileFieldEditing() {
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".edit-pencil-container")) {
      handleBioDropdownMenu();
    }
  });
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
  const searchResults = document.getElementById('user-search-results');
  searchResults.innerHTML = '';

  let foundMatch = false;

  for (const user of users) {
    const searchResultsLink = document.createElement('a');
    searchResultsLink.href = '/user_profile/' + user.username + '/';
    searchResultsLink.textContent = user.first_name + ' ' + user.last_name;
    const searchResultsList = document.createElement('li');
    searchResultsList.appendChild(searchResultsLink);
    searchResults.appendChild(searchResultsList);

    foundMatch = true;
  }


}

// FUNC - 8: UPDATE IMAGE PREVIEW
function handleUpdateImagePreview(event) {
  const imageFileInput = event.target;
  const imageFile = imageFileInput.files[0];
  const imagePreview = document.getElementById('image-preview');

  if (imageFile) {
    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
    };
    reader.readAsDataURL(imageFile);
  } else {
    imagePreview.src = '';
  }
}

// EVENT 1: PROFILE DETAILS - EDIT BIO
document.addEventListener("click", (event) => {
  if (!event.target.closest(".edit-pencil-container")) {
    handleBioDropdownMenu();
  }
});

// EVENT 2: PROFILE DETAILS
document.querySelectorAll("[data-field-name]").forEach((profileFieldElement) => {
  profileFieldElement.addEventListener("change", () => {
    const profileFieldName = profileFieldElement.getAttribute("data-field-name");
    const profileFieldsNewValue = profileFieldElement.getAttribute("data-value");
    sendUpdatedValueToServer(profileFieldName, profileFieldsNewValue);
  });
});

// EVENT 3: DROPDOWN MENU
document.querySelectorAll(".dropdown-menu a").forEach(function (menuItem) {
  menuItem.addEventListener("click", function (event) {
    event.preventDefault();

    const profileFieldDropdownMenu = event.target.parentElement;
    const profileFieldName = profileFieldDropdownMenu.getAttribute("data-field-name");
    const profileFieldElement = document.querySelector(`[data-field-name="${profileFieldName}"]`);
    const profileFieldSelectedValue = event.target.getAttribute("data-value");

    handleUpdateProfileField(profileFieldElement, profileFieldSelectedValue, event.target.textContent);
    profileFieldDropdownMenu.style.display = "none";
  });
});

// EVENT 4: EDIT-PENCIL - DROPDOWN MENU
document.querySelectorAll(".edit-pencil").forEach(function (pencil) {
  pencil.addEventListener("click", function (event) {
    event.preventDefault();
    event.stopPropagation();

    handleBioDropdownMenu();

    const profileFieldDropdownMenu = pencil.nextElementSibling;
    if (profileFieldDropdownMenu.style.display === "none" || profileFieldDropdownMenu.style.display === "") {
      profileFieldDropdownMenu.style.display = "block";
    } else {
      profileFieldDropdownMenu.style.display = "none";
    }
  });
});

// EVENT 5: FILE INPUT CHANGE
const imageFileInput = document.getElementById('file-input');
if (imageFileInput) {
  imageFileInput.addEventListener('change', handleUpdateImagePreview);
}

// EVENT: DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  handleBioEditing();
  initProfileFieldEditing();

  const searchInput = document.getElementById('user-search-input');
  const searchResults = document.getElementById('user-search-results');

  if (searchInput && searchResults) {
    function handleSearchInput(event) {
      const query = event.target.value.trim();
      if (query.length === 0) {
        handleUserSearchResults([]);
      } else {
        handleUserSearch(query);
      }
    }

    function handleSearchResults(event) {
      const selectedUserInSearchResults = event.target.value;
      if (selectedUserInSearchResults) {
        window.location.href = `/user_profile/${selectedUserInSearchResults}/`;
      }
    }

    // Attach event listeners
    searchInput.addEventListener('input', handleSearchInput);
    searchResults.addEventListener('change', handleSearchResults);
  }

  const postLikeForm = document.getElementById('post-like-form');
  const postLikeButton = document.getElementById('post-like-btn');
  const postLikeCount = document.getElementById('post-like-count');

  if (postLikeForm && postLikeButton && postLikeCount) {
    postLikeForm.addEventListener('submit', (event) => {
      event.preventDefault();

      const postId = postLikeButton.getAttribute('data-post-id');
      const postLikeUrl = `/post_details/toggle-like/${postId}/`;

      fetch(postLikeUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
        },
      })
        .then(response => response.json())
        .then(data => {
          postLikeButton.classList.toggle('liked', data.post_like_status);
          postLikeButton.textContent = data.post_like_status ? 'Unlike' : 'Like';
          postLikeCount.textContent = data.like_count;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  }
});
