(function () {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
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
  function initializeCommentInput() {
    document.querySelectorAll(".comment-btn").forEach((button) => {
      button.addEventListener("click", () => {
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
      });
    });
  }
  function updateProfileField(fieldElement, newValue, newTextContent) {
    fieldElement.setAttribute("data-value", newValue);
    fieldElement.textContent = newTextContent;
    const fieldName = fieldElement.getAttribute("data-field-name");
    sendUpdatedValueToServer(fieldName, newValue);
  }
  
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
  
  // FUNCTION: EDIT-PENCIL - BIO
  function initializeBioEditing() {
    const editPencilBio = document.querySelector('.edit-pencil-bio');
    // EVENT: EDIT-PENCIL - BIO
    if (editPencilBio) {
      editPencilBio.addEventListener('click', function (event) {
        event.preventDefault();
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

  document.addEventListener('DOMContentLoaded', function () {
    initializeCropper();
    likePost();
    initializeCommentInput();
    initializeBioEditing();


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
})();