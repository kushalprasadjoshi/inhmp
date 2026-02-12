document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('searchBtn').addEventListener('click', searchPatients);
    document.getElementById('visitForm').addEventListener('submit', createVisit);
    document.getElementById('visitDate').valueAsDate = new Date();

    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/';
    });
});

async function searchPatients() {
    const query = document.getElementById('searchQuery').value;
    if (query.length < 2) return;
    try {
        const patients = await apiFetch(`/patients/search?q=${encodeURIComponent(query)}`);
        const resultsDiv = document.getElementById('searchResults');
        resultsDiv.innerHTML = '';
        if (patients.length === 0) {
            resultsDiv.innerHTML = '<div class="alert alert-warning">No patients found</div>';
            return;
        }
        const list = document.createElement('ul');
        list.className = 'list-group';
        patients.forEach(p => {
            const item = document.createElement('li');
            item.className = 'list-group-item list-group-item-action';
            item.innerHTML = `<strong>${p.full_name}</strong> (${p.national_id || 'No ID'}) - DOB: ${p.date_of_birth}`;
            item.addEventListener('click', () => selectPatient(p));
            list.appendChild(item);
        });
        resultsDiv.appendChild(list);
    } catch (err) {
        alert('Search failed: ' + err.message);
    }
}

function selectPatient(patient) {
    document.getElementById('patientId').value = patient.id;
    document.getElementById('selectedPatient').value = `${patient.full_name} (${patient.national_id})`;
    document.getElementById('searchResults').innerHTML = ''; // clear results
}

async function createVisit(e) {
    e.preventDefault();
    const patientId = document.getElementById('patientId').value;
    if (!patientId) {
        alert('Please select a patient');
        return;
    }
    const data = {
        patient_id: patientId,
        visit_date: document.getElementById('visitDate').value,
        diagnosis_code: document.getElementById('diagnosisCode').value,
        symptoms: document.getElementById('symptoms').value,
        treatment: document.getElementById('treatment').value,
        medication: document.getElementById('medication').value,
        lab_result: document.getElementById('labResult').value,
        is_emergency: document.getElementById('isEmergency').checked
    };
    try {
        await apiFetch('/visits', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        alert('Visit saved successfully!');
        document.getElementById('visitForm').reset();
        document.getElementById('visitDate').valueAsDate = new Date();
    } catch (err) {
        alert('Failed to save visit: ' + err.message);
    }
}