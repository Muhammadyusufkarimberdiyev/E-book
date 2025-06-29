const loginForm = document.querySelector('.login-container');
const registerForm = document.querySelector('.register-container');
const switchToRegister = document.getElementById('switch-to-register');
const switchToLogin = document.getElementById('switch-to-login');

// Show register form and hide login form
switchToRegister.addEventListener('click', (e) => {
    e.preventDefault();
    loginForm.classList.remove('active');
    registerForm.classList.add('active');
});

// Show login form and hide register form
switchToLogin.addEventListener('click', (e) => {
    e.preventDefault();
    registerForm.classList.remove('active');
    loginForm.classList.add('active');
});

function addToCart(bookId) {
    alert("Book with ID " + bookId + " added to cart!");
    // Add actual logic to add to cart here
}
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-favorite").forEach(button => {
        button.addEventListener("click", function () {
            let itemId = this.dataset.id;
            removeFromFavorites(itemId);
        });
    });

    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            let bookId = this.dataset.id;
            addToCart(bookId);
        });
    });
});

// 🗑 Favorite-dan o‘chirish
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
            document.getElementById(`favorite-item-${itemId}`).remove(); // O‘chirib tashlash
        } else {
            alert("Error removing favorite.");
        }
    })
    .catch(error => console.error("Error:", error));
}

// 🛒 Cart-ga qo‘shish
function addToCart(bookId) {
    fetch(`/cart/add/${bookId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Book added to cart!");
        } else {
            alert("Error adding to cart.");
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

function removeFromCart(itemId) {
    alert("Item with ID " + itemId + " removed from cart!");
    // Add actual logic to remove from cart here
}

// Set initial state
loginForm.classList.add('active');

// LOGIN FUNCTION
async function loginUser(username, password) {
    try {
        const response = await fetch('http://127.0.0.1:8000/auth/token/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Saqlash token
            localStorage.setItem('authToken', data.auth_token);
            alert('Login successful!');
        } else {
            alert('Login failed: ' + data.non_field_errors[0]);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong!');
    }
}

// LOGIN FORM EVENT
document.querySelector('#login-btn').addEventListener('click', (e) => {
    e.preventDefault();
    const username = document.querySelector('#login-username').value;
    const password = document.querySelector('#login-password').value;
    loginUser(username, password);
});



// REGISTER FUNCTION
async function registerUser(username, password) {
    try {
        const response = await fetch('http://127.0.0.1:8000/auth/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Registration successful! Please login.');
            // Switch to login form
            registerForm.classList.remove('active');
            loginForm.classList.add('active');
        } else {
            alert('Registration failed: ' + data.username[0]);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong!');
    }
}

// REGISTER FORM EVENT
document.querySelector('#register-btn').addEventListener('click', (e) => {
    e.preventDefault();
    const username = document.querySelector('#register-username').value;
    const password = document.querySelector('#register-password').value;
    registerUser(username, password);
});


// LOGOUT FUNCTION
async function logoutUser() {
    const token = localStorage.getItem('authToken');

    if (!token) {
        alert('You are not logged in!');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/token/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`,
            }
        });

        if (response.ok) {
            // Remove token
            localStorage.removeItem('authToken');
            alert('Logged out successfully!');
        } else {
            alert('Logout failed!');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong!');
    }
}

// LOGOUT BUTTON EVENT
document.querySelector('#logout-btn').addEventListener('click', (e) => {
    e.preventDefault();
    logoutUser();
});

