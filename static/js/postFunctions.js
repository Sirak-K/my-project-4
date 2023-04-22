// FILE: postFunctions.js

// IMPORTS
import {
    toggleComments,
    fetchAndDisplayComments
} from './postComment.js';
import { getCookie } from './utility.js';



// FILE: postFunctions.js

// IMPORTS
import {
  toggleComments,
  fetchAndDisplayComments
} from './postComment.js';
import { getCookie } from './utility.js';

// CSRF Token
const csrfToken = getCookie('csrftoken');




// -- FUNC-1: POST-CREATION
async function createPost(e) {
e.preventDefault();

const form = e.target;
const formData = new FormData(form);

// IMPLEMENT LOGIC FOR CREATING A POST
const response = await fetch(form.action, {
  method: 'POST',
  headers: {
    'X-CSRFToken': csrfToken
  },
  body: formData
});

const data = await response.json();

// CALL SUB-FUNCTIONS TO HANDLE POST CREATION DETAILS
const postId = data.id;
appendLikesToCreatedPost(postId);
appendCommentsToCreatedPost(postId);
  handlePostRemovalButton(postId);
  
// Append the new post to the existing list of posts
const postList = document.getElementById('post-list');
const postItem = document.createElement('div');
postItem.classList.add('post-item');
postItem.innerHTML = `
  <div>
    <h3>${data.title}</h3>
    <<p>${data.content}</p>
    <span>Likes: ${data.likes}</span>
  </div>
`;
postList.insertBefore(postItem, postList.firstChild);

// Clear the form fields
form.reset();

}


// FUNC-1 A
function appendLikesToCreatedPost(postId) {
// IMPLEMENT LOGIC TO APPEND LIKES TO CREATED POST
const likeBtn = document.querySelector(`.like-btn[data-post-id="${postId}"]`);
likeBtn.addEventListener('click', () => {
  // Call the function that handles liking a post
});
}


// FUNC-1 B
function appendCommentsToCreatedPost(postId) {
// IMPLEMENT LOGIC TO APPEND COMMENTS TO CREATED POST
const commentForm = document.querySelector(`.post-comment-form[data-post-id="${postId}"]`);
commentForm.addEventListener('submit', (e) => {
  e.preventDefault();
  // Call the function that handles adding a comment to a post
});
}


// FUNC-1 C
function handlePostRemovalButton(postId) {
// IMPLEMENT LOGIC FOR POST REMOVAL BUTTON
// INCLUDING CONFIRMATION WINDOW AND MODAL
const removeBtn = document.querySelector(`.btn-remove-post-${postId}`);
removeBtn.addEventListener('click', async () => {
  if (confirm('Are you sure you want to remove this post?')) {
    // Call the function that handles post removal
    await removePost(postId);
  }
});
}




// -- FUNC-2: POST-SUBMISSION
async function submitPost(postData) {
// IMPLEMENT LOGIC TO SUBMIT POST TO DATABASE
const response = await fetch('/post_create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken
  },
  body: JSON.stringify(postData)
});

const data = await response.json();
return data;
}

// -- FUNC-3: POST LIST - DISPLAY POSTS
async function displayPostList() {
// RETRIEVE DATA FROM DATABASE
const posts = await fetchAllCreatedPosts();

// DISPLAY ALL CREATED POSTS
displayAllCreatedPosts(posts);
}
// FUNC-3 A
async function fetchAllCreatedPosts() {
// IMPLEMENT LOGIC TO FETCH ALL CREATED POSTS
// FROM "FUNC-1"
const response = await fetch('/api/post_list/');
const data = await response.json();
return data;
}
// FUNC-3 B
function displayAllCreatedPosts(posts) {
  // IMPLEMENT LOGIC TO DISPLAY ALL CREATED POSTS
  const postList = document.getElementById('post-list');
  
  for (const post of posts) {
    const postItem = document.createElement('div');
    postItem.classList.add('post-item');
    
    // Replace this line with actual HTML content of the post.
    // You may use a template string or a separate function to build the HTML content
    postItem.innerHTML = `
      <div>
        <h3>${post.title}</h3>
        <p>${post.content}</p>
        <span>Likes: ${post.likes}</span>
      </div>
    `;
    
    postList.appendChild(postItem);
  }
}

// Event Listener #1
document.querySelector('.create-post-form').addEventListener('submit', createPost);

// Event Listener #5
window.addEventListener('DOMContentLoaded', displayPostList);

// EXPORTS
export { 
  createPost,
  appendLikesToCreatedPost,
  appendCommentsToCreatedPost,
  handlePostRemovalButton,
  submitPost,
  displayPostList,
  fetchAllCreatedPosts,
  displayAllCreatedPosts
};
