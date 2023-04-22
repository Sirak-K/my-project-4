// FILE: profileDetails.js

// FUNC - 1: PROFILE DETAIL - BIO - EDIT-PENCIL
function initBioEditing() {
    const editPencilBio = document.querySelector('.edit-pencil-bio');
    // EVENT: EDIT-PENCIL - BIO
    if (editPencilBio) {
    editPencilBio.addEventListener('click', function (event) {
    event.preventDefault();
    event.stopPropagation();
    closeOpenDropdownAndDisableBio();
    
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
// FUNC - 2: PROFILE DETAIL - CLOSE DROPDOWN
function closeOpenDropdownAndDisableBio() {
document.querySelectorAll(".dropdown-menu").forEach((dropdown) => {
    dropdown.style.display = "none";
});

const bioElement = document.querySelector("[data-field-name='bio']");
if (bioElement && bioElement.getAttribute("contenteditable") === "true") {
    bioElement.blur();
}
}
// FUNC - 3: PROFILE DETAILS
function updateProfileField(fieldElement, newValue, newTextContent) {
fieldElement.setAttribute("data-value", newValue);
fieldElement.textContent = newTextContent;
const fieldName = fieldElement.getAttribute("data-field-name");
sendUpdatedValueToServer(fieldName, newValue);
}
// FUNC - 4: PROFILE DETAILS - SAVE DETAIL
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
function initProfileDetailsEventListeners() {
    // EVENT 1: PROFILE DETAILS - EDIT BIO
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".edit-pencil-container")) {
        closeOpenDropdownAndDisableBio();
      }
    });
  
    // ... (other event listeners) ...
}

// EVENT 1: PROFILE DETAILS - EDIT BIO
document.addEventListener("click", (event) => {
    if (!event.target.closest(".edit-pencil-container")) {
    closeOpenDropdownAndDisableBio();
    }
});
// EVENT 2: PROFILE DETAILS
document.querySelectorAll("[data-field-name]").forEach((fieldElement) => {
fieldElement.addEventListener("change", () => {
const fieldName = fieldElement.getAttribute("data-field-name");
const newValue = fieldElement.getAttribute("data-value");
sendUpdatedValueToServer(fieldName, newValue);
});
});
// EVENT 3: DROPDOWN MENU
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
// EVENT 4: EDIT-PENCIL - DROPDOWN MENU
document.querySelectorAll(".edit-pencil").forEach(function (pencil) {
pencil.addEventListener("click", function (event) {
event.preventDefault();
event.stopPropagation();

closeOpenDropdownAndDisableBio();

const dropdownMenu = pencil.nextElementSibling;
if (dropdownMenu.style.display === "none" || dropdownMenu.style.display === "") {
    dropdownMenu.style.display = "block";
} else {
    dropdownMenu.style.display = "none";
}
});
});

export {
    initBioEditing,
    initProfileDetailsEventListeners
};
