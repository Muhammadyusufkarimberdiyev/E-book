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



// // Show register form and hide login form
// switchToRegister.addEventListener('click', (e) => {
//     e.preventDefault();
//     loginForm.classList.remove('active');
//     registerForm.classList.add('active');
// });

// // Show login form and hide register form
// switchToLogin.addEventListener('click', (e) => {
//     e.preventDefault();
//     registerForm.classList.remove('active');
//     loginForm.classList.add('active');
// });

// // Set initial state
// loginForm.classList.add('active');

// // LOGIN FUNCTION
// async function loginUser(username, password) {
//     try {
//         const response = await fetch('http://127.0.0.1:8000/auth/token/login/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 username: username,
//                 password: password
//             })
//         });

//         const data = await response.json();

//         if (response.ok) {
//             // Save token
//             localStorage.setItem('authToken', data.auth_token);
//             alert('Login successful!');
//         } else {
//             alert('Login failed: ' + (data.non_field_errors ? data.non_field_errors[0] : 'Unknown error'));
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('Something went wrong!');
//     }
// }

// // REGISTER FUNCTION
// async function registerUser(username, email, password) {
//     try {
//         const response = await fetch('http://127.0.0.1:8000/auth/users/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 username: username,
//                 email: email,
//                 password: password
//             })
//         });

//         const data = await response.json();

//         if (response.ok) {
//             alert('Registration successful! Please login.');
//             // Switch to login form
//             registerForm.classList.remove('active');
//             loginForm.classList.add('active');
//         } else {
//             alert('Registration failed: ' + (data.username ? data.username[0] : 'Unknown error'));
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('Something went wrong!');
//     }
// }

// // LOGIN FORM EVENT
// document.querySelector('#login-form').addEventListener('submit', (e) => {
//     e.preventDefault();
//     const username = document.querySelector('#login-username').value;
//     const password = document.querySelector('#login-password').value;
//     loginUser(username, password);
// });

// // REGISTER FORM EVENT
// document.querySelector('#register-form').addEventListener('submit', (e) => {
//     e.preventDefault();
//     const username = document.querySelector('#register-username').value;
//     const email = document.querySelector('#register-email').value;
//     const password = document.querySelector('#register-password').value;
//     registerUser(username, email, password);
// });
