// FILE: script.js

// IMPORTS
import {
  initBioEditing
} from './profileDetails.js';

import {
  fetchAndDisplayPosts,
  likePost,
  RemovePostConfirmation,
  submitPost,
  initPostsWithComments
} from './postFunctions.js';

import {
  initCommentFormListener,
} from './postComment.js';


import {
  getCookie
} from './utility.js';




// EVENT: DOMContentLoaded
document.addEventListener('DOMContentLoaded', async function () {
  likePost();
  initBioEditing();
  RemovePostConfirmation();
  initCommentFormListener(getCookie);

  // Initialize the event listener for form submission
  document.querySelector('#create-post-form').addEventListener('submit', submitPost);

  // Call initPostsWithComments to fetch and display posts and their comments
  await initPostsWithComments();

});


