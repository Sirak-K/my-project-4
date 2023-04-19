
// FUNC -  1: UTILITY ~ COOKIE
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// FUNC - 1: PROFILE DETAIL - BIO - EDIT-PENCIL
function initializeBioEditing() {
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
// FUNC - 3: PROFILE DETAILS
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

fetch(`/user_profile/${user_id}/update_field/`, {
method: "POST",
body: JSON.stringify(data),
headers: {
"Content-Type": "application/json",
"X-CSRFToken": getCookie("csrftoken"), // Include the CSRF token
},
})
.then((response) => {
if (!response.ok) {
  throw new Error("Network response was not ok");
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
// FUNC - 5: POST - LIKE
function likePost() {
  document.querySelectorAll(".like-btn").forEach((btn) => {
  btn.addEventListener("click", async () => {
  const postId = btn.dataset.postId;
  const response = await fetch(`/post_like/${postId}/`, { method: "POST" });
  const data = await response.json();
  btn.textContent = `Like (${data.likes})`;
  
  // Update the displayed like count
  const likeCountElement = document.querySelector(`#like-count-${postId}`);
  likeCountElement.textContent = data.likes;
  });
  });
}
// FUNC - 6: POST REMOVAL - CONFIRMATION WINDOW
function confirmRemovePost() {
  return confirm("Are you sure you want to remove the post?");
}
// FUNC - 7: POST REMOVAL - CONFIRMATION BUTTON
function RemovePostConfirmation() {
  document.querySelectorAll(".remove-post-btn").forEach((btn) => {
    btn.addEventListener("click", (event) => {
      if (!confirmRemovePost()) {
        event.preventDefault(); // Prevent form submission if the user doesn't confirm
      }
    });
  });
}

// FUNC - 8: COMMENTS - TOGGLE VISIBILITY
function toggleComments(event) {
  if (!event || !event.target) {
    console.error("toggleComments was called without an event or event target");
    return;
  }

  const commentToggleContainerId = event.target.getAttribute('data-container');
  const commentToggleContainerElement = document.getElementById(commentToggleContainerId);
  commentToggleContainerElement.style.display = commentToggleContainerElement.style.display === "none" ? "block" : "none";
}



// -------------- /// -------------- //// -------------- /// -------------- //

// EVENT: DOMContentLoaded
document.addEventListener('DOMContentLoaded', function () {
likePost();
initializeBioEditing();
RemovePostConfirmation();

  
  // FUNC - 9: COMMENTS - CREATION
  function createCommentElement(postId, user, content, date) {
    console.log('Creating comment element for postId:', postId);
    const commentElement = document.createElement('div');
    commentElement.classList.add('comment');
  
    const userElement = document.createElement('div');
    userElement.classList.add('comment-user');
    userElement.textContent = user;
  
    const contentElement = document.createElement('div');
    contentElement.classList.add('comment-content');
    contentElement.textContent = content;
  
    const dateElement = document.createElement('div');
    dateElement.classList.add('comment-date');
    dateElement.textContent = date;
  
    commentElement.appendChild(userElement);
    commentElement.appendChild(contentElement);
    commentElement.appendChild(dateElement);
  
    const commentListContainer = document.getElementById(`post-comment-list-section-${postId}`);
    commentListContainer.appendChild(commentElement);
  
    return commentElement;
  }
  
  
// Inside DOMContentLoaded event listener
const commentForm = document.querySelector(".post-comment-form");
if (commentForm) {

  commentForm.addEventListener("submit", async (event) => {
    console.log("Submit event triggered"); // Add this line
        event.preventDefault();

        const contentInput = event.target.querySelector(".post-comment-input");
        const content = contentInput.value;
        const postId = event.target.action.split("/").slice(-2)[0];

        // Submit the comment using fetch
        const response = await fetch(event.target.action, {
            method: "POST",
            body: JSON.stringify({ content }),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        });

        if (response.ok) {
          // KARIS-2: APPEND NEW COMMENT
          const commentData = await response.json();
          console.log("Finding comment list container for postId:", postId);

          const commentListContainer = document.getElementById(`post-comment-list-section-${postId}`);
          console.log(`Trying to find comment list container with id: post-comment-list-section-${postId}`);
          console.log('commentListContainer:', commentListContainer);
          
          const commentElement = createCommentElement(postId, commentData.user, commentData.content, commentData.date);
          
          console.log('commentContainer:', commentListContainer);
          console.log("Appending comment element to:", commentListContainer);

          commentListContainer.appendChild(commentElement);
          contentInput.value = ""; // Clear the input field
      } else {
          console.error("Error submitting comment");
      }
      
    });
}

  // EVENT: COMMENTS - TOGGLE VISIBLITY (BY PRESSING SPEECH BUBBLE ICON)
document.querySelectorAll(".btn-toggle-comment").forEach((btn) => {
  btn.addEventListener("click", toggleComments);
});

  
// EVENT: PROFILE DETAILS
document.querySelectorAll("[data-field-name]").forEach((fieldElement) => {
fieldElement.addEventListener("change", () => {
const fieldName = fieldElement.getAttribute("data-field-name");
const newValue = fieldElement.getAttribute("data-value");
sendUpdatedValueToServer(fieldName, newValue);
});
});
// EVENT: EDIT-PENCIL - DROPDOWN MENU
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


// Add event listeners to the dropdown menu items
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

// EVENT: POST CONTENT - "SHOW MORE"-button
const showMoreButtons = document.querySelectorAll('.btn-show-more');

showMoreButtons.forEach((button) => {
const postText = button.previousElementSibling;
const postHeight = postText.offsetHeight;
const fullHeight = postText.scrollHeight;

if (postHeight >= fullHeight) {
button.style.display = 'none';
}

button.addEventListener('click', () => {
if (postText.style.height === '60px') {
  postText.style.height = `${fullHeight}px`;
  button.textContent = 'Show Less';
} else {
  postText.style.height = '60px';
  button.textContent = 'Show More';
}
});
});
})

// EVENT: PROFILE DETAILS - EDIT BIO
document.addEventListener("click", (event) => {
if (!event.target.closest(".edit-pencil-container")) {
closeOpenDropdownAndDisableBio();
}
});


// -------------- /// -------------- //// -------------- /// -------------- //