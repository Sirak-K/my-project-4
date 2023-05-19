// File: script.js

// IMPORTS
import {
  initBioEditing
} from './profileDetails.js';


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
    const url = `/post/${postId}/toggle-like/`;

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

function getCookie(name) {
  const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return cookieValue ? cookieValue.pop() : '';
}
});