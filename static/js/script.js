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

function toggleCommentInput(button) {
  const input = button.nextElementSibling;
  input.style.display = input.style.display === "none" ? "block" : "none";
  input.addEventListener("keydown", async (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const postId = button.parentElement.dataset.postId;
      const content = input.value;
      const response = await fetch(`/post_comment/${postId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ content: content }),
      });
      if (response.ok) {
        input.value = "";

        // Update the displayed comment count
        const commentCountElement = document.querySelector(
          `#comment-count-${postId}`
        );
        commentCountElement.textContent = parseInt(commentCountElement.textContent) + 1;

        // Optionally, refresh the page or update the comments section.
      }
    }
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
