///////////// AUTHENTICATION LOGIC //////////////////
document.addEventListener('DOMContentLoaded', () => {
    loadHospitals();

    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const data = {
            full_name: form.fullName.value,
            email: form.email.value,
            phone: form.phone.value,
            password: form.password.value,
            role: form.role.value,
            hospital_id: form.hospitalId.value || null
        };

        try {
            const result = await apiFetch('/auth/register', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showMessage('Registration successful! Redirecting to login...', 'success');
            setTimeout(() => window.location.href = '/pages/login.html', 2000);
        } catch (err) {
            showMessage(err.message, 'danger');
        }
    });
});

async function loadHospitals() {
    try {
        const hospitals = await apiFetch('/hospitals'); // will implement later
        const select = document.getElementById('hospitalId');
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

function showMessage(msg, type) {
    const msgDiv = document.getElementById('registerMessage');
    msgDiv.className = `mt-3 alert alert-${type}`;
    msgDiv.textContent = msg;
    msgDiv.classList.remove('d-none');
}