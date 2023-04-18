(function () {
// FUNC -  1: UTILITY ~ COOKIE
function getCookie(name) {
const value = `; ${document.cookie}`;
const parts = value.split(`; ${name}=`);
if (parts.length === 2) return parts.pop().split(';').shift();
  }
// FUNC - 2: POST - COMMENTS
async function postComment(submitCommentButton) {
  const commentInputSection = submitCommentButton.closest(".comment-input-section");
  const commentInput = commentInputSection.querySelector(".comment-input");
  const postId = commentInputSection.dataset.postId;
  const content = commentInput.value;

  const response = await fetch(`/post_comment/${postId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ content: content }),
  });

  if (response.ok) {
    const data = await response.json();

    const newComment = document.createElement("div");
    newComment.classList.add("comment");
    newComment.innerHTML = `
      <p class="comment-content">${data.content}</p>
      <p class="comment-timestamp">${data.created_date}</p>
    `;

    const commentContainer = document.querySelector(`#comment-container-${postId}`);
    commentContainer.appendChild(newComment);

    const commentCountElement = document.querySelector(`#comment-count-${postId}`);
    const commentCount = parseInt(commentCountElement.textContent, 10) + 1;
    commentCountElement.textContent = commentCount;

    commentInput.value = "";
  } else {
    console.error("Error posting comment:", await response.text());
  }
}
// FUNC - 3: POST - COMMENTS - READ POSTS
async function readPostComments(postId) {
  const response = await fetch(`/post_comments/${postId}/`);

  if (response.ok) {
    const comments = await response.json();

    // Get the comments section for the specified post
    const commentsSection = document.querySelector(`.post[data-post-id="${postId}"] .comments-section`);
    commentsSection.innerHTML = '';

    comments.forEach((comment) => {
      // Create the comment HTML element
      const commentElement = document.createElement('div');
      commentElement.classList.add('comment');
      commentElement.innerHTML = `
        <p class="comment-content">${comment.content}</p>
        <p class="comment-timestamp">${comment.timestamp}</p>
      `;

      // Append the comment HTML element to the comments section
      commentsSection.appendChild(commentElement);
    });

  } else {
    console.error('Error retrieving comments:', response.statusText);
  }
}
// FUNC - 4: POST - COMMENTS - GET POSTS
async function getPosts() {
  const response = await fetch('/posts/');

  if (response.ok) {
    const posts = await response.json();

    posts.forEach((post) => {
      // Create the post HTML element
      const postElement = document.createElement('div');
      postElement.classList.add('post');
      postElement.dataset.postId = post.id;
      postElement.innerHTML = `
        <button class="btn-show-comments">Show Comments</button>
        <div class="comments-section" style="display:none;"></div>
      `;

      // Append the post HTML element to the DOM
      const postContainer = document.querySelector('.post-container');
      postContainer.appendChild(postElement);

      
    });
  } else {
    console.error('Error retrieving posts:', response.statusText);
  }
}
// FUNC - 5: POST - COMMENTS - TOGGLE VISIBILITY
function toggleCommentsSection(button) {
  const commentsSection = button.nextElementSibling;
  if (commentsSection.style.display === "none") {
    commentsSection.style.display = "block";
    button.textContent = "Hide Comments";
    const postId = button.closest('.post').dataset.postId;
    if (commentsSection.children.length === 0) {
      readPostComments(postId);
    }
  } else {
    commentsSection.style.display = "none";
    button.textContent = "Show Comments";
  }
}
  
  
// FUNC - 6: POST - COMMENTS - SUBMISSION / INPUT
function submitCommentHandler(event, submitCommentButton) {
  event.preventDefault();
  const commentInputSection = event.target.closest(".comment-input-section");
  const commentInput = commentInputSection.querySelector(".comment-input");
  const postId = commentInputSection.dataset.postId;
  const content = commentInput.value;

  if (content.trim() === "") {
    alert("Please enter a comment.");
    return;
  }

  (async () => {
    const response = await fetch(`/post_comment/${postId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ content: content }),
    });

    if (response.ok) {
      // Call the postComment function here, passing the submitCommentButton
      await postComment(submitCommentButton);
      commentInput.value = "";
    } else {
      console.error("Error posting comment:", await response.text());
    }
  })();
}

document.querySelectorAll('.btn-submit-comment').forEach((button) => {
  button.addEventListener('click', (event) => {
    submitCommentHandler(event, button);
  });
});

document.querySelectorAll('.btn-show-comments').forEach((button) => {
  button.addEventListener('click', () => {
    toggleCommentsSection(button);
  });
});


// FUNC - 7: PROFILE IMAGE - CROPPER
function initializeCropper() {
  const editImageButton = document.getElementById('btn-edit-image');
  const saveChangesButton = document.getElementById('btn-save-changes');
  
  // Check if elements exist before adding event listeners
  if (editImageButton && saveChangesButton) {
  editImageButton.addEventListener('click', () => {
  const image = document.getElementById('uploaded-image');
  const cropper = new Cropper(image, {
    aspectRatio: 1,
    viewMode: 1,
    autoCropArea: 1,
    cropBoxResizable: false,
    dragMode: 'move',
    crop(event) {
      // You can access the cropping data here
    },
  });
  
  saveChangesButton.style.display = 'block';
  editImageButton.style.display = 'none';
  
  saveChangesButton.addEventListener('click', () => {
    const croppedImageDataUrl = cropper.getCroppedCanvas().toDataURL();
    // Save the cropped image data
    // You can now send this croppedImageDataUrl to the server to save the new profile image
    // ...
    cropper.destroy();
    saveChangesButton.style.display = 'none';
    editImageButton.style.display = 'block';
  });
  });
  }
}
// FUNC - 8: POST - LIKE
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
// FUNC - 9: PROFILE DETAILS
function updateProfileField(fieldElement, newValue, newTextContent) {
fieldElement.setAttribute("data-value", newValue);
fieldElement.textContent = newTextContent;
const fieldName = fieldElement.getAttribute("data-field-name");
sendUpdatedValueToServer(fieldName, newValue);
}
// FUNC - 10: PROFILE DETAILS - SAVE DETAIL
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
// FUNC - 11: PROFILE DETAIL - CLOSE DROPDOWN
function closeOpenDropdownAndDisableBio() {
  document.querySelectorAll(".dropdown-menu").forEach((dropdown) => {
    dropdown.style.display = "none";
  });

  const bioElement = document.querySelector("[data-field-name='bio']");
  if (bioElement && bioElement.getAttribute("contenteditable") === "true") {
    bioElement.blur();
  }
}
// FUNC - 12: EDIT-PENCIL - BIO
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
// FUNC - 13: POST REMOVAL - CONFIRMATION WINDOW
function confirmRemovePost() {
  return confirm("Are you sure you want to remove the post?");
}
// FUNC - 14: POST REMOVAL - CONFIRMATION BUTTON
function RemovePostConfirmation() {
  document.querySelectorAll(".remove-post-btn").forEach((btn) => {
    btn.addEventListener("click", (event) => {
      if (!confirmRemovePost()) {
        event.preventDefault(); // Prevent form submission if the user doesn't confirm
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', function () {
initializeCropper();
likePost();
initializeBioEditing();
RemovePostConfirmation();
getPosts();

  
  
// EVENT: POST - SHOW COMMENTS 
document.querySelectorAll(".btn-show-comments").forEach((button) => {
  const commentsCount = parseInt(button.getAttribute("data-comments-count"), 10);

  if (commentsCount === 0) {
    button.style.display = "none";
  } else {
    button.style.display = "block";
    button.addEventListener("click", () => {
      toggleCommentsSection(button);
    });
  }
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

// EVENT: POST - "SHOW MORE"-button
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
document.addEventListener("click", (event) => {
if (!event.target.closest(".edit-pencil-container")) {
closeOpenDropdownAndDisableBio();
}
});
})();