// patient.js – handles profile loading and logout
document.addEventListener('DOMContentLoaded', async () => {
    // ===== LOAD PATIENT PROFILE =====
    const profileCard = document.getElementById('profileCard');
    if (profileCard) {
        try {
            const profile = await apiFetch('/patients/me');
            document.getElementById('fullName').textContent = profile.full_name || '-';
            document.getElementById('email').textContent = profile.email || '-';
            document.getElementById('phone').textContent = profile.phone || '-';
            document.getElementById('nationalId').textContent = profile.national_id || '-';
            document.getElementById('dob').textContent = profile.date_of_birth || '-';
            document.getElementById('bloodGroup').textContent = profile.blood_group || '-';
            document.getElementById('allergies').textContent = profile.allergies || '-';
            document.getElementById('emergencyContact').textContent = profile.emergency_contact || '-';
        } catch (err) {
            console.error('Failed to load profile:', err);
            const container = document.querySelector('.container');
            if (container) {
                container.innerHTML = `<div class="alert alert-danger">Failed to load profile: ${err.message}</div>`;
            }
        }
    }

    // ===== LOGOUT BUTTON =====
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('access_token');
            window.location.href = '/';
        });
    }
});