// auth.js – handles registration and login
document.addEventListener('DOMContentLoaded', () => {
    // ===== REGISTRATION FORM =====
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        loadHospitalsDropdown(); // defined below
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const data = {
                full_name: form.fullName.value,
                email: form.email.value,
                phone: form.phone.value,
                password: form.password.value,
                role: form.role.value,
                hospital_id: form.hospitalId?.value || null
            };
            try {
                await apiFetch('/auth/register', {
                    method: 'POST',
                    body: JSON.stringify(data)
                });
                showRegisterMessage('Registration successful! Redirecting to login...', 'success');
                setTimeout(() => window.location.href = '/pages/login.html', 2000);
            } catch (err) {
                showRegisterMessage(err.message, 'danger');
            }
        });
    }

    // ===== LOGIN FORM =====
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            try {
                const result = await apiFetch('/auth/login', {
                    method: 'POST',
                    body: JSON.stringify({ email, password })
                });
                localStorage.setItem('access_token', result.access_token);
                // Decode token for role-based redirect
                try {
                    const payload = JSON.parse(atob(result.access_token.split('.')[1]));
                    const role = payload.role;
                    showLoginMessage('Login successful! Redirecting...', 'success');
                    setTimeout(() => {
                        const redirects = {
                            'Patient': '/pages/patient_profile.html',
                            'Doctor': '/pages/visit_entry.html',
                            'HospitalAdmin': '/pages/hospital_dashboard.html',
                            'EmergencyOfficer': '/pages/emergency_override.html',
                            'SystemAdmin': '/pages/audit_logs.html'
                        };
                        window.location.href = redirects[role] || '/';
                    }, 1500);
                } catch (e) {
                    // fallback redirect
                    window.location.href = '/';
                }
            } catch (err) {
                showLoginMessage(err.message, 'danger');
            }
        });
    }
});

// ===== HOSPITALS DROPDOWN =====
async function loadHospitalsDropdown() {
    const select = document.getElementById('hospitalId');
    if (!select) return;
    try {
        const hospitals = await apiFetch('/hospitals');
        hospitals.forEach(h => {
            const option = document.createElement('option');
            option.value = h.id;
            option.textContent = h.name;
            select.appendChild(option);
        });
    } catch (err) {
        console.error('Failed to load hospitals', err);
    }
}

// ===== REGISTER MESSAGE =====
function showRegisterMessage(msg, type) {
    const msgDiv = document.getElementById('registerMessage');
    if (msgDiv) {
        msgDiv.className = `mt-3 alert alert-${type}`;
        msgDiv.textContent = msg;
        msgDiv.classList.remove('d-none');
        setTimeout(() => msgDiv.classList.add('d-none'), 5000);
    }
}

// ===== LOGIN MESSAGE =====
function showLoginMessage(msg, type) {
    const msgDiv = document.getElementById('loginMessage');
    if (msgDiv) {
        msgDiv.className = `mt-3 alert alert-${type}`;
        msgDiv.textContent = msg;
        msgDiv.classList.remove('d-none');
        setTimeout(() => msgDiv.classList.add('d-none'), 5000);
    }
}