document.addEventListener('DOMContentLoaded', () => {
    loadHospitals();

    const form = document.getElementById('hospitalForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('name').value,
                district: document.getElementById('district').value,
                address: document.getElementById('address').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value
            };
            try {
                await apiFetch('/hospitals', {
                    method: 'POST',
                    body: JSON.stringify(data)
                });
                showMessage('Hospital registered successfully!', 'success');
                form.reset();
                loadHospitals(); // refresh list
            } catch (err) {
                showMessage(err.message, 'danger');
            }
        });
    }

    document.getElementById('logoutBtn')?.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/';
    });
});

async function loadHospitals() {
    try {
        const hospitals = await apiFetch('/hospitals');
        const list = document.getElementById('hospitalList');
        list.innerHTML = '';
        hospitals.forEach(h => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `${h.name} <span class="badge bg-secondary">${h.district}</span>`;
            list.appendChild(li);
        });
    } catch (err) {
        console.error('Failed to load hospitals', err);
    }
}

function showMessage(msg, type) {
    const msgDiv = document.getElementById('hospitalMessage');
    msgDiv.className = `mt-3 alert alert-${type}`;
    msgDiv.textContent = msg;
    msgDiv.classList.remove('d-none');
    setTimeout(() => msgDiv.classList.add('d-none'), 5000);
}