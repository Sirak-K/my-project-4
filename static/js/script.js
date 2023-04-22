// FILE: script.js

// IMPORTS
import {
  initBioEditing
} from './profileDetails.js';

import {
  createPost,
  appendLikesToCreatedPost,
  appendCommentsToCreatedPost,
  handlePostRemovalButton,
  submitPost,
  displayPostList,
  fetchAllCreatedPosts,
  displayAllCreatedPosts
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
  handlePostRemovalButton(); // Updated function name
  initCommentFormListener(getCookie);
  displayPostList(); // Updated function name
});
