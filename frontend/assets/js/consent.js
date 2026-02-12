document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('requestOtpForm').addEventListener('submit', requestOtp);
    document.getElementById('verifyOtpForm').addEventListener('submit', verifyOtp);
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/';
    });
});

async function requestOtp(e) {
    e.preventDefault();
    const data = {
        patient_id: document.getElementById('patientIdRequest').value,
        accessing_hospital_id: document.getElementById('accessingHospitalId').value
    };
    try {
        const result = await apiFetch('/consent/request-otp', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        // Populate consent ID and show OTP (mock)
        document.getElementById('consentId').value = result.consent_id;
        const otpDiv = document.getElementById('otpResult');
        otpDiv.innerHTML = `<div class="alert alert-info">OTP generated (mock): <strong>${result.otp}</strong></div>`;
    } catch (err) {
        alert('Request failed: ' + err.message);
    }
}

async function verifyOtp(e) {
    e.preventDefault();
    const data = {
        consent_id: document.getElementById('consentId').value,
        otp: document.getElementById('otpCode').value
    };
    try {
        const result = await apiFetch('/consent/verify-otp', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        document.getElementById('verifyResult').innerHTML = 
            `<div class="alert alert-success">${result.message}</div>`;
        // Optionally redirect to patient records
    } catch (err) {
        alert('Verification failed: ' + err.message);
    }
}