// ============= LOGIN HANDLER =============
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Clear any previous messages
        const msgDiv = document.getElementById('loginMessage');
        if (msgDiv) msgDiv.classList.add('d-none');

        try {
            const result = await apiFetch('/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });

            console.log('Login success:', result);
            localStorage.setItem('access_token', result.access_token);

            // Decode token to get role (optional, but recommended for role-based redirect)
            const token = result.access_token;
            const payload = JSON.parse(atob(token.split('.')[1]));
            const role = payload.role;
            console.log('User role:', role);

            // Show success message
            if (msgDiv) {
                msgDiv.className = 'mt-3 alert alert-success';
                msgDiv.textContent = 'Login successful! Redirecting...';
                msgDiv.classList.remove('d-none');
            }

            // Redirect based on role
            setTimeout(() => {
                switch(role) {
                    case 'Patient':
                        window.location.href = '/pages/patient_profile.html';
                        break;
                    case 'Doctor':
                        window.location.href = '/pages/visit_entry.html';
                        break;
                    case 'HospitalAdmin':
                        window.location.href = '/pages/hospital_dashboard.html';
                        break;
                    case 'EmergencyOfficer':
                        window.location.href = '/pages/emergency_override.html';
                        break;
                    case 'SystemAdmin':
                        window.location.href = '/pages/audit_logs.html';
                        break;
                    default:
                        window.location.href = '/';
                }
            }, 1500);

        } catch (err) {
            console.error('Login error:', err);
            if (msgDiv) {
                msgDiv.className = 'mt-3 alert alert-danger';
                msgDiv.textContent = err.message || 'Login failed. Please check your credentials.';
                msgDiv.classList.remove('d-none');
            }
        }
    });
}