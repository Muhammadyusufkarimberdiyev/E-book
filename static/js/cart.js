function updateCart(itemId, action) {
    fetch(`/update-cart/${itemId}/${action}/`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) location.reload();
    });
}

function removeFromCart(itemId) {
    fetch(`/remove-cart/${itemId}/`, { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) location.reload();
    });
}



function removeFromFavorites(itemId) {
    fetch(`/favorites/remove/${itemId}/`, { 
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // HTML-dan o‘chirish
            document.getElementById(`favorite-item-${itemId}`).remove();
        } else {
            alert("Failed to remove item from favorites.");
        }
    })
    .catch(error => console.error("Error:", error));
}

// CSRF token olish (Django uchun)
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}


document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".update-quantity").forEach(button => {
        button.addEventListener("click", function () {
            let itemId = this.dataset.id;
            let action = this.dataset.action;
            updateCart(itemId, action);
        });
    });

    document.querySelectorAll(".remove-item").forEach(button => {
        button.addEventListener("click", function () {
            let itemId = this.dataset.id;
            removeFromCart(itemId);
        });
    });
});

// 🛒 Cartni yangilash
function updateCart(itemId, action) {
    fetch(`/cart/update/${itemId}/${action}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Sahifani yangilash (tezkor natija)
        } else {
            alert("Error updating cart.");
        }
    })
    .catch(error => console.error("Error:", error));
}

// 🗑 Cartdan o‘chirish
function removeFromCart(itemId) {
    fetch(`/cart/remove/${itemId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`cart-item-${itemId}`).remove(); // Elementni olib tashlash
        } else {
            alert("Error removing item.");
        }
    })
    .catch(error => console.error("Error:", error));
}

// 🔑 CSRF token olish (Django uchun)
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}
