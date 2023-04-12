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

// AUTO-SAVE: PROFILE DETAILS
$(document).ready(function() {
  function autoSaveProfileField(field_name, field_value) {
    $.ajax({
      url: '{% url "user_profile_field_update" user_profile.user.id %}',
      method: 'POST',
      data: {
        'field_name': field_name,
        'field_value': field_value,
        'csrfmiddlewaretoken': '{{ csrf_token }}'
      },
      success: function(data) {
        if (data.status === 'success') {
          console.log('Profile field updated successfully');
        } else {
          console.error('Error updating profile field:', data.message);
        }
      }
    });
  }

  function makeEditable(element) {
    element.setAttribute('contenteditable', 'true');
    element.focus();
  }

  function makeUneditable(element) {
    element.removeAttribute('contenteditable');
    autoSaveProfileField(element.dataset.fieldName, element.textContent.trim());
  }

  $('.edit-pencil').click(function(event) {
    event.preventDefault();
    const fieldElement = document.querySelector(this.dataset.fieldSelector);
    makeEditable(fieldElement);
  });

  $('[data-field-name]').blur(function() {
    makeUneditable(this);
  });
});

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('#update-profile-form');
  if (!form) return;

  const editElements = document.querySelectorAll('.edit-pencil, .edit-image');
  for (const editElement of editElements) {
    editElement.addEventListener('click', function(event) {
      event.preventDefault();

      const fieldName = editElement.getAttribute('data-field-name');
      const fieldSelector = editElement.getAttribute('data-field-selector');

      const activeField = document.querySelector('.active-edit-field');
      if (activeField) {
        activeField.classList.remove('active-edit-field');
      }

      const formField = document.querySelector(fieldSelector);
      formField.classList.add('active-edit-field');

      formField.focus();
      if (formField.tagName === 'INPUT' || formField.tagName === 'TEXTAREA') {
        formField.select();
      }

      formField.addEventListener('input', autoSave);
      formField.addEventListener('change', autoSave);
      formField.addEventListener('blur', autoUpdate);
    });
  }

  function autoSave(event) {
    const formField = event.target;

    const form = formField.closest('form');
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    const fieldName = formField.getAttribute('data-field-name');
    const fieldValue = formField.value;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', form.getAttribute('data-url'), true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        const response = JSON.parse(xhr.responseText);
        if (response.status === 'success') {
          console.log('Profile field updated successfully');
        } else {
          console.error('Error updating profile field:', response.message);
        }
      }
    };

    xhr.send(`field_name=${encodeURIComponent(fieldName)}&field_value=${encodeURIComponent(fieldValue)}`);
  }

  function autoUpdate(event) {
    const formField = event.target;
    formField.classList.remove('active-edit-field');
  }
});
