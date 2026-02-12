// patient.js – handles profile loading and logout
document.addEventListener('DOMContentLoaded', async () => {
    // ===== PATIENT PROFILE VIEW =====
    const profileCard = document.getElementById('profileCard');
    if (profileCard) {
        loadPatientProfile();
    }

    async function loadPatientProfile() {
        try {
            const profile = await apiFetch('/patients/me');
            // populate fields...
            document.getElementById('fullName').textContent = profile.full_name || '-';
            // ... all other fields
        } catch (err) {
            console.error('Profile load error:', err);
            // ✅ If profile not found (404), redirect to registration
            if (err.message.includes('404') || err.message.includes('Patient profile not found')) {
                window.location.href = '/pages/patient_registration.html';
            } else {
                // Other errors show message
                const container = document.querySelector('.container');
                if (container) {
                    container.innerHTML = `<div class="alert alert-danger">Failed to load profile: ${err.message}</div>`;
                }
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