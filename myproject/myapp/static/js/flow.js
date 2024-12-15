const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelectorAll('.login-link'); // Updated to select all login links
const registerLink = document.querySelector('.register-link');
const forgotLink = document.querySelector('.forgot-link');
const btnPopup = document.querySelector('.btnLoginpopup');
const iconClose = document.querySelector('.icon-close');

console.log('Script is Connected')

// To open the popup
btnPopup.addEventListener('click', () => {
    wrapper.classList.add('active-popup');
});

// To close the popup
iconClose.addEventListener('click', () => {
    wrapper.classList.remove('active-popup');
});

// Show login form on default
const showLoginForm = () => {
    wrapper.querySelector('.login').style.display = 'block'; // Show login
    wrapper.querySelector('.register').style.display = 'none'; // Hide register
    wrapper.querySelector('.forgot').style.display = 'none'; // Hide forgot password
};

// Show registration form
registerLink.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default link behavior
    wrapper.querySelector('.login').style.display = 'none'; // Hide login
    wrapper.querySelector('.register').style.display = 'block'; // Show register
    wrapper.querySelector('.forgot').style.display = 'none'; // Hide forgot password
});

// Show forgot password form
forgotLink.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default link behavior
    wrapper.querySelector('.login').style.display = 'none'; // Hide login
    wrapper.querySelector('.register').style.display = 'none'; // Hide register
    wrapper.querySelector('.forgot').style.display = 'block'; // Show forgot password
});

// Show login form when any login link is clicked
loginLink.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default link behavior
        showLoginForm(); // Show login form
    });
});

// Initialize to show login form when the page loads
showLoginForm();
