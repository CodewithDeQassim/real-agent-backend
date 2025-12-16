// Frontend JavaScript for connecting to Real Agent Backend API

const API_BASE = window.location.origin;

// Example: Fetch user statistics on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Frontend connected to backend at:', API_BASE);

    // Example API call - get user statistics
    fetchUserStats();
});

// Function to fetch user statistics from backend
async function fetchUserStats() {
    try {
        const response = await fetch(`${API_BASE}/stats/users`);
        if (response.ok) {
            const stats = await response.json();
            console.log('User statistics:', stats);
            // You can update the UI here with the stats
            displayUserStats(stats);
        } else {
            console.error('Failed to fetch user stats');
        }
    } catch (error) {
        console.error('Error fetching user stats:', error);
    }
}

// Function to display user statistics in the UI
function displayUserStats(stats) {
    // Example: Add a stats section to the page
    const heroSection = document.querySelector('.hero');
    if (heroSection && stats) {
        const statsDiv = document.createElement('div');
        statsDiv.className = 'user-stats';
        statsDiv.innerHTML = `
            <p><strong>Total Users:</strong> ${stats.total_users}</p>
            <p><strong>Active Users:</strong> ${stats.active_users}</p>
        `;
        heroSection.appendChild(statsDiv);
    }
}

// Example login function
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();
        if (result.success) {
            console.log('Login successful:', result.user);
            // Store user session, redirect, etc.
        } else {
            console.error('Login failed:', result.message);
        }
        return result;
    } catch (error) {
        console.error('Login error:', error);
    }
}

// Example: Add login form functionality (you would add HTML form first)
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }
}

// Initialize login form when DOM is ready
document.addEventListener('DOMContentLoaded', setupLoginForm);