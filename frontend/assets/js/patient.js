// ===== PATIENT REGISTRATION – 100% WORKING =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ patient.js loaded');

    // ----- REGISTRATION FORM -----
    const form = document.getElementById('patientForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('📝 Form submitted');

            const data = {
                national_id: document.getElementById('nationalId')?.value || '',
                date_of_birth: document.getElementById('dob')?.value,
                blood_group: document.getElementById('bloodGroup')?.value || '',
                allergies: document.getElementById('allergies')?.value || '',
                emergency_contact: document.getElementById('emergencyContact')?.value || ''
            };
            console.log('📦 Payload:', data);

            const msgDiv = document.getElementById('patientMessage');
            if (msgDiv) {
                msgDiv.className = 'mt-3 alert alert-info';
                msgDiv.textContent = '⏳ Submitting...';
                msgDiv.classList.remove('d-none');
            }

            const token = localStorage.getItem('access_token');
            console.log('🔑 Token present:', !!token);
            if (!token) {
                alert('Not logged in. Redirecting...');
                window.location.href = '/pages/login.html';
                return;
            }

            try {
                const response = await fetch('/patients/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(data)
                });

                const responseData = await response.json().catch(() => ({}));
                console.log('📡 Response:', response.status, responseData);

                if (!response.ok) {
                    throw new Error(responseData.detail || `HTTP ${response.status}`);
                }

                console.log('✅ Registration success');
                if (msgDiv) {
                    msgDiv.className = 'mt-3 alert alert-success';
                    msgDiv.textContent = '✅ Profile created! Redirecting...';
                    msgDiv.classList.remove('d-none');
                }
                setTimeout(() => {
                    window.location.href = '/pages/patient_profile.html';
                }, 1500);
            } catch (err) {
                console.error('❌ Error:', err);
                if (msgDiv) {
                    msgDiv.className = 'mt-3 alert alert-danger';
                    msgDiv.textContent = `❌ ${err.message}`;
                    msgDiv.classList.remove('d-none');
                }
            }
        });
    }

    // ----- PROFILE PAGE -----
    if (document.getElementById('profileCard')) {
        loadProfile();
    }
});

async function loadProfile() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) throw new Error('No token');

        const response = await fetch('/patients/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Profile not found');
        const profile = await response.json();

        document.getElementById('fullName').textContent = profile.full_name || '-';
        document.getElementById('email').textContent = profile.email || '-';
        document.getElementById('phone').textContent = profile.phone || '-';
        document.getElementById('nationalId').textContent = profile.national_id || '-';
        document.getElementById('dob').textContent = profile.date_of_birth || '-';
        document.getElementById('bloodGroup').textContent = profile.blood_group || '-';
        document.getElementById('allergies').textContent = profile.allergies || '-';
        document.getElementById('emergencyContact').textContent = profile.emergency_contact || '-';
    } catch (err) {
        console.error('Profile load error:', err);
        // If no profile, redirect to registration
        if (err.message.includes('404') || err.message.includes('not found')) {
            window.location.href = '/pages/patient_registration.html';
        }
    }
}