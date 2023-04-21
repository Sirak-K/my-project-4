// FILE: script.js

// IMPORTS
import {
  initBioEditing
} from './profileDetails.js';

import {
  fetchAndDisplayPosts,
  likePost,
  RemovePostConfirmation,
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
  fetchAndDisplayPosts();


});


