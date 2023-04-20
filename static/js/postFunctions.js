// FILE: postFunctions.js

// IMPORTS
import {
    toggleComments,
    fetchAndDisplayComments
} from './postComment.js';
import { getCookie } from './utility.js';


// FUNC - 1: POST - LIKES
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
// FUNC - 2: POST - REMOVAL - CONFIRMATION WINDOW
function confirmRemovePost() {
return confirm("Are you sure you want to remove the post?");
}
// FUNC - 3: POST - REMOVAL - CONFIRMATION BUTTON
function RemovePostConfirmation() {
document.querySelectorAll(".remove-post-btn").forEach((btn) => {
    btn.addEventListener("click", (event) => {
    if (!confirmRemovePost()) {
        event.preventDefault(); // Prevent form submission if the user doesn't confirm
    }
    });
});
}

// FUNC - 5: POST - INITIALIZE EVENTS
function initPostEvents(postId) {
    likePost(postId);
    RemovePostConfirmation(postId);
}


// FUNC - 6: POST - FETCH & DISPLAY
async function fetchAndDisplayPosts(page = 1) {
  const response = await fetch(`/api/posts/?page=${page}`);
  if (response.ok) {
    const postData = await response.json();
    const postList = document.querySelector("#post-list");

    // Clear the existing posts
    postList.innerHTML = "";

    // Check if postData has 'posts' property and it is iterable
    if (postData.posts && Array.isArray(postData.posts)) {
      for (const post of postData.posts) {
        createAndAppendNewPost(post, postList);
      }
      return Array.from(postList.children); // Return the post elements
    } else {
      console.error("Unexpected response format:", postData);
      return []; // Return an empty array if the response is not as expected
    }
  } else {
    console.error("Error fetching posts");
    return []; // Return an empty array if the response is not ok
  }
   // Update the current page and total pages in the pagination controls
   document.querySelector('#current-page').textContent = postData.current_page;
   document.querySelector('#total-pages').textContent = postData.total_pages;
}


// FUNC - 7 - POST - SUBMIT
async function submitPost(event) {
event.preventDefault();

const form = event.target;
const formData = new FormData(form);
const url = form.action;

try {
    const response = await fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
    },
    body: formData,
    });

    if (response.ok) {
    const jsonResponse = await response.json();
    if (jsonResponse.status === 'success') {
        // Add the new post to the list
        const newPost = jsonResponse.post;
        displayNewPost(newPost);
        form.reset();
    } else {
        // Handle errors
        console.error('Error in response:', jsonResponse);
    }
    } else {
    console.error('Error submitting form:', response.statusText);
    }
} catch (error) {
    console.error('Error submitting form:', error);
}
}
// FUNC - 8 - POST - DISPLAY NEW POSTS
function displayNewPost(newPost) {
const postList = document.querySelector('#post-list');

// Get the template element and its content
const postItemTemplate = document.getElementById('post-item-template');
const templateContent = postItemTemplate.content;

// Populate the template with data
templateContent.querySelector('.post-author').textContent = newPost.fields.author.get_full_name;
templateContent.querySelector('.post-content').textContent = newPost.fields.content;
templateContent.querySelector('.post-date').textContent = newPost.fields.created_at;

// Clone the template content and append it to the post list
const postItem = document.importNode(templateContent, true);
postList.appendChild(postItem);
}

// FUNC - 9 - POST - INIT POSTS 
async function initPostsWithComments() {
    // Fetch and display posts
    const postElements = await fetchAndDisplayPosts();
  
    // Fetch and display comments for each post
    for (const postElement of postElements) {
      const postId = postElement.dataset.postId;
      await fetchAndDisplayComments(postId, postElement);
  }


  // Add click event listeners for the pagination controls
document.querySelector('#pagination-controls .first').addEventListener('click', async (event) => {
  event.preventDefault();
  await fetchAndDisplayPosts(1);
});

document.querySelector('#pagination-controls .previous').addEventListener('click', async (event) => {
  event.preventDefault();
  const currentPage = parseInt(document.querySelector('#current-page').textContent, 10);
  await fetchAndDisplayPosts(Math.max(currentPage - 1, 1));
});

document.querySelector('#pagination-controls .next').addEventListener('click', async (event) => {
  event.preventDefault();
  const currentPage = parseInt(document.querySelector('#current-page').textContent, 10);
  const totalPages = parseInt(document.querySelector('#total-pages').textContent, 10);
  await fetchAndDisplayPosts(Math.min(currentPage + 1, totalPages));
});

document.querySelector('#pagination-controls .last').addEventListener('click', async (event) => {
  event.preventDefault();
  const totalPages = parseInt(document.querySelector('#total-pages').textContent, 10);
  await fetchAndDisplayPosts(totalPages);
});

}
  


// EXPORTS
export {
    likePost,
    RemovePostConfirmation,
    fetchAndDisplayPosts,
    submitPost,
    initPostEvents,
    initPostsWithComments
};
