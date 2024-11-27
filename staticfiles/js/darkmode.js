const toggleSwitch = document.getElementById('darkModeToggle');

// Check for saved user preference in localStorage
if (localStorage.getItem('darkMode') === 'enabled') {
    document.body.classList.add('dark-mode');
    applyDarkModeStyles();
}

// Add event listener for the toggle switch
toggleSwitch.addEventListener('change', () => {
    if (toggleSwitch.checked) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('darkMode', 'enabled');
        applyDarkModeStyles();
        console.log('Dark mode activated');
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('darkMode', 'disabled');
        removeDarkModeStyles();
        console.log('Dark mode deactivated');
    }
});

// Function to apply dark mode styles inline
function applyDarkModeStyles() {
    document.body.style.backgroundColor = '#121212'; // Dark background
    document.body.style.color = '#ffffff'; // Light text
    const headers = document.querySelectorAll('header, footer, main');
    headers.forEach(header => {
        header.style.backgroundColor = '#1e1e1e'; // Darker background for header and footer
        header.style.color = '#ffffff'; // Light text for headers
    });
}

// Function to remove dark mode styles
function removeDarkModeStyles() {
    document.body.style.backgroundColor = ''; // Reset background
    document.body.style.color = ''; // Reset text color
    const headers = document.querySelectorAll('header, footer, main');
    headers.forEach(header => {
        header.style.backgroundColor = ''; // Reset background for headers
        header.style.color = ''; // Reset text color for headers
    });
}
