document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('emergencyForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            patient_id: document.getElementById('patientId').value,
            reason: document.getElementById('reason').value,
            justification: document.getElementById('justification').value
        };
        try {
            const result = await apiFetch('/emergency/access', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showMessage(`Emergency access granted. Log ID: ${result.id}`, 'success');
            document.getElementById('emergencyForm').reset();
        } catch (err) {
            showMessage(err.message, 'danger');
        }
    });

    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/';
    });
});

function showMessage(msg, type) {
    const msgDiv = document.getElementById('emergencyMessage');
    msgDiv.className = `mt-3 alert alert-${type}`;
    msgDiv.textContent = msg;
    msgDiv.classList.remove('d-none');
    setTimeout(() => msgDiv.classList.add('d-none'), 5000);
}