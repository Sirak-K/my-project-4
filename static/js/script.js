// File: script.js

function getCookie(name) {
  // FUNC : 1: Get the value of a cookie
  const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return cookieValue ? cookieValue.pop() : '';
}

function handleProfileBioEdit() {
  const editPencilBio = document.querySelector('.edit-pencil-bio');
  
  if (editPencilBio) {
    editPencilBio.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      handleProfileBioAndProfileDropdownMenus();

      const bioElement = document.querySelector("[data-field-name='bio']");
      bioElement.focus();
    });
  }

  const bioElement = document.querySelector("[data-field-name='bio']");
  if (bioElement) {
    bioElement.addEventListener('blur', () => {
      const profileFieldsNewValue = bioElement.textContent;
      sendUpdatedFieldValueToServer('bio', profileFieldsNewValue);
    });
  }
}

function handleProfileBioAndProfileDropdownMenus() {
  document.querySelectorAll(".dropdown-menu").forEach((dropdown) => {
    dropdown.style.display = "none";
  });

  const bioElement = document.querySelector("[data-field-name='bio']");
  if (bioElement && bioElement.getAttribute("contenteditable") === "true") {
    bioElement.blur();
  }
}

function handleUpdateProfileField(profileFieldElement, profileFieldsNewValue, newTextContent) {
  profileFieldElement.setAttribute("data-value", profileFieldsNewValue);
  profileFieldElement.textContent = newTextContent;
  const profileFieldName = profileFieldElement.getAttribute("data-field-name");
  sendUpdatedFieldValueToServer(profileFieldName, profileFieldsNewValue);
}

function sendUpdatedFieldValueToServer(profileFieldName, profileFieldsNewValue) {
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

function initProfileFieldEdit() {
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".edit-pencil-container")) {
      handleProfileBioAndProfileDropdownMenus();
    }
  });
}

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

function handleUserSearchResults(users) {
  const searchResults = document.getElementById('user-search-results');
  searchResults.innerHTML = '';

  let foundMatch = false;

  for (const user of users) {
    const userSearchResultsLink = document.createElement('a');
    userSearchResultsLink.href = '/user_profile/' + user.username + '/';
    userSearchResultsLink.textContent = user.first_name + ' ' + user.last_name;
    const searchResultsList = document.createElement('li');
    searchResultsList.appendChild(userSearchResultsLink);
    searchResults.appendChild(searchResultsList);

    foundMatch = true;
  }
}

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

function handlePostLikeForm() {
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
        // Update the button state based on the server response
        postLikeButton.classList.toggle('liked', data.post_like_status);
        postLikeButton.textContent = data.post_like_status ? 'Unlike' : 'Like';

        // Update the like count
        postLikeCount.textContent = data.like_count;

        // Update the database state
        postLikesUpdateDatabaseState(postId, data.post_like_status);
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });

    // Retrieve the initial database state and update the button state
    const postId = postLikeButton.getAttribute('data-post-id');
    const initialPostLikeStatus = postLikesGetDatabaseState(postId);
    postLikeButton.classList.toggle('liked', initialPostLikeStatus);
    postLikeButton.textContent = initialPostLikeStatus ? 'Unlike' : 'Like';
  }
}

function postLikesGetDatabaseState(postId) {
  const databaseState = localStorage.getItem(`post-like-state-${postId}`);
  return databaseState === 'true';
}

function postLikesUpdateDatabaseState(postId, postLikeStatus) {
  localStorage.setItem(`post-like-state-${postId}`, postLikeStatus);
}

// Handle profile details click event for editing profile field bio
document.addEventListener("click", (event) => {
  if (!event.target.closest(".edit-pencil-container")) {
    handleProfileBioAndProfileDropdownMenus();
  }
});

//  Handle profile details change event for profile field
document.querySelectorAll("[data-field-name]").forEach((profileFieldElement) => {
  profileFieldElement.addEventListener("change", () => {
    const profileFieldName = profileFieldElement.getAttribute("data-field-name");
    const profileFieldsNewValue = profileFieldElement.getAttribute("data-value");
    sendUpdatedFieldValueToServer(profileFieldName, profileFieldsNewValue);
  });
});

// Handle profile details dropdown menu item click event
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

// Handle edit-pencil click event to toggle dropdown menu
document.querySelectorAll(".edit-pencil").forEach(function (pencil) {
  pencil.addEventListener("click", function (event) {
    event.preventDefault();
    event.stopPropagation();

    handleProfileBioAndProfileDropdownMenus();

    const profileFieldDropdownMenu = pencil.nextElementSibling;
    if (profileFieldDropdownMenu.style.display === "none" || profileFieldDropdownMenu.style.display === "") {
      profileFieldDropdownMenu.style.display = "block";
    } else {
      profileFieldDropdownMenu.style.display = "none";
    }
  });
});

// Handle profile image upload file input change
const imageFileInput = document.getElementById('file-input');
if (imageFileInput) {
  imageFileInput.addEventListener('change', handleUpdateImagePreview);
}

// DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  handleProfileBioEdit();
  initProfileFieldEdit();

  handlePostLikeForm();

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
});
