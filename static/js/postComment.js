// FILE: postComment.js

// FUNC - 1: COMMENTS - CREATION
function createCommentElement(postId, user, content, date) {
    const commentElement = document.createElement("div");
    commentElement.classList.add("comment");
    commentElement.dataset.postId = postId;
  
    const commentUser = document.createElement("span");
    commentUser.classList.add("comment-user");
    commentUser.textContent = user;
  
    const commentContent = document.createElement("span");
    commentContent.classList.add("comment-content");
    commentContent.textContent = content;
  
    const commentDate = document.createElement("span");
    commentDate.classList.add("comment-date");
    commentDate.textContent = date;
  
    commentElement.appendChild(commentUser);
    commentElement.appendChild(commentContent);
    commentElement.appendChild(commentDate);
  
    return commentElement;
}
// FUNC - 2: COMMENTS - TOGGLE VISIBILITY
function toggleComments(event) {
  const postId = event.target.dataset.postId;
  const commentsContainer = document.querySelector(`.post-comment-container[data-post-id="${postId}"]`);
  commentsContainer.classList.toggle("hidden");

  // Find the existing toggle comments button by postId
  const toggleCommentsBtn = document.querySelector(`.btn-toggle-comment[data-post-id="${postId}"]`);
  
  // Add the event listener to the existing button
  if (toggleCommentsBtn) {
    toggleCommentsBtn.removeEventListener("click", toggleComments);
    toggleCommentsBtn.addEventListener("click", toggleComments);
  }

  // Fetch and display comments when toggling visibility
  fetchAndDisplayComments(postId);
}
// FUNC - 3: COMMENTS - INITIALIZE COMMENT FORM
function initCommentFormListener(getCookie) {
    const commentForms = document.querySelectorAll(".post-comment-form");
    if (commentForms) {
      commentForms.forEach((commentForm) => {
        commentForm.addEventListener("submit", async (event) => {
          event.preventDefault();
  
          const postId = event.target.dataset.postId;
          const csrfToken = getCookie("csrftoken");
          const commentContent = event.target.querySelector(".post-comment-input").value;
  
          const response = await fetch("/api/comments/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
              post: postId,
              content: commentContent,
            }),
          });
  
          if (response.ok) {
            const newComment = await response.json();
            const commentElement = createCommentElement(postId, newComment.user, newComment.content, newComment.date);
            const commentsContainer = document.querySelector(`.post-comment-container[data-post-id="${postId}"]`);
            commentsContainer.appendChild(commentElement);
            event.target.querySelector(".post-comment-input").value = "";
          } else {
            console.error("Error submitting comment");
          }
        });
      });
    }
  
}
// FUNC - 4: COMMENTS - FETCH & DISPLAY
async function fetchAndDisplayComments(postId, postElement) {
  const response = await fetch(`/api/comments/?post=${postId}`);
  if (response.ok) {
    const commentsData = await response.json();
    const commentsContainer = postElement.querySelector('.post-comment-container'); // updated query selector
    commentsContainer.innerHTML = ""; // clear previous comments<
    for (const commentData of commentsData.comments) {
      const commentElement = createCommentElement(postId, commentData.user, commentData.content, commentData.date);
      commentsContainer.appendChild(commentElement);
    }
  } else {
    console.error('Error fetching comments');
  }
}



// EVENT: COMMENTS - TOGGLE VISIBILITY (BY PRESSING SPEECH BUBBLE ICON)
document.querySelectorAll(".btn-toggle-comment").forEach((btn) => {
    btn.addEventListener("click", toggleComments);
});

// EXPORTS
export {
  initCommentFormListener,
  toggleComments,
  fetchAndDisplayComments
};
