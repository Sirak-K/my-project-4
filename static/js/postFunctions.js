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
// FUNC - 2: POST - REMOVAL - CONFIRMATION BUTTON
function RemovePostConfirmation() {
  const removeBtns = document.querySelectorAll('.btn-remove-post');

  removeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const postId = btn.getAttribute('data-post-id');
      const modal = document.querySelector(`#post-remove-modal-${postId}`);
      modal.style.display = 'block';

      // Add event listeners for the confirmation and cancel buttons
      modal.querySelector('.btn-post-remove-confirm').addEventListener('click', async () => {
        // Call your function to remove the post here
        
        modal.style.display = 'none';
      });

      modal.querySelector('.btn-post-remove-cancel').addEventListener('click', () => {
        modal.style.display = 'none';
      });
    });
  });
}
// FUNC - 3: POST - INITIALIZE EVENTS
function initPostEvents(postId) {
    likePost(postId);
    RemovePostConfirmation(postId);
}
// FUNC - 4: POST - FETCH & DISPLAY
async function fetchAndDisplayPosts(page = 1) {
  const response = await fetch(`/post_list/?page=${page}`);
  if (response.ok) {
    const renderedPosts = await response.text(); // Get the rendered HTML as text
    const postList = document.querySelector("#post-list");

    // Update the post list with the rendered HTML
    postList.innerHTML = renderedPosts;

    // Update the current page and total pages in the pagination controls
    // These values should be part of the rendered HTML or returned separately as JSON data.
    // The following code assumes you have the values as data attributes on the post-list element.
    document.querySelector('#current-page').textContent = postList.dataset.currentPage;
    document.querySelector('#total-pages').textContent = postList.dataset.totalPages;

    return Array.from(postList.children); // Return the post elements
  } else {
    console.error("Error fetching posts");
    return []; // Return an empty array if the response is not ok
  }
}

// FUNC - 5 - POST - SUBMIT
async function submitPost(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);
  const url = '/post_create/';

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
      console.log('Server response:', jsonResponse); // Debugging statement 1

      if (jsonResponse.status === 'success' && jsonResponse.post) {
        // Add the new post to the list
        const postData = jsonResponse.post; // Extract the post object from the response
        createAndAppendNewPost(postData)
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

// FUNC - 6 - POST - HANDLE CREATION OF NEW POSTS
function createAndAppendNewPost(postData) {

  // DEBUGGING
  console.log('createAndAppendNewPost: postData:', postData);
  console.log('post content:', postData.fields.content); 

  // Get the post item template
  const postItemTemplate = document.getElementById('post-item-template').content.cloneNode(true);

  // Update the post details
  postItemTemplate.querySelector('.post-author').textContent = postData.fields.author.get_full_name;
  postItemTemplate.querySelector('.post-content').textContent = postData.fields.content;
  postItemTemplate.querySelector('.post-date').textContent = postData.fields.time_since_posted;

  // Append the updated post item template to the post-list section
  const postListSection = document.getElementById('post-list');
  postListSection.appendChild(postItemTemplate);

  console.log('Post created:', postData); // Debugging statement
}




// FUNC - 7 - POST - INIT POSTS 
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
  
 // Initialize the event listener for form submission
 document.addEventListener('DOMContentLoaded', () => {
  const createPostForm = document.querySelector('#create-post-form');
  if (createPostForm) {
    createPostForm.addEventListener('submit', submitPost);
  }
});

// EXPORTS
export {
    likePost,
    RemovePostConfirmation,
    fetchAndDisplayPosts,
    submitPost,
    initPostEvents,
    initPostsWithComments,
    createAndAppendNewPost
};



  // // Update the author image
  // const authorImage = postItemTemplate.querySelector('.post-author-image');
  // if (postData.fields.author.profile && postData.fields.author.profile.profile_image_url) {
  //   authorImage.src = postData.fields.author.profile.profile_image_url;
  //   authorImage.alt = postData.fields.author.get_full_name;
  // } else {
  //   authorImage.src = "/media/img/default_profile_image.png";
  //   authorImage.alt = "";
  // }

  // // Add post image if it exists
  // if (postData.fields.image_url) {
  //   const postImage = postItemTemplate.querySelector('.post-image');
  //   postImage.src = postData.image_url;
  //   postImage.alt = "Post Image";
  // }