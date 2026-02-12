// ml_demo.js – handle form submissions and update UI

document.addEventListener('DOMContentLoaded', () => {
    // Check login status
    const token = localStorage.getItem('access_token');
    const userStatus = document.getElementById('userStatus');
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');

    if (token) {
        // Decode token to get email (optional)
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            userStatus.textContent = `👤 ${payload.email || 'User'}`;
        } catch {
            userStatus.textContent = '👤 Logged in';
        }
        loginBtn.classList.add('d-none');
        logoutBtn.classList.remove('d-none');
    } else {
        userStatus.textContent = '👤 Guest';
        loginBtn.classList.remove('d-none');
        logoutBtn.classList.add('d-none');
    }

    // Logout handler
    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('access_token');
        window.location.reload();
    });

    // Diabetes form submission
    const diabetesForm = document.getElementById('diabetesForm');
    if (diabetesForm) {
        diabetesForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(diabetesForm);
            const features = {
                pregnancies: parseFloat(formData.get('pregnancies')),
                glucose: parseFloat(formData.get('glucose')),
                blood_pressure: parseFloat(formData.get('blood_pressure')),
                skin_thickness: parseFloat(formData.get('skin_thickness')),
                insulin: parseFloat(formData.get('insulin')),
                bmi: parseFloat(formData.get('bmi')),
                diabetes_pedigree: parseFloat(formData.get('diabetes_pedigree')),
                age: parseFloat(formData.get('age'))
            };

            const resultDiv = document.getElementById('diabetesResult');
            resultDiv.innerHTML = '<div class="alert alert-info">⏳ Predicting...</div>';

            try {
                const response = await apiFetch('/ml/predict/diabetes', {
                    method: 'POST',
                    body: JSON.stringify(features)
                });
                renderDiabetesResult(resultDiv, response);
            } catch (err) {
                resultDiv.innerHTML = `<div class="alert alert-danger">❌ Error: ${err.message}</div>`;
            }
        });
    }

    // Heart form submission
    const heartForm = document.getElementById('heartForm');
    if (heartForm) {
        heartForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(heartForm);
            const features = {
                age: parseFloat(formData.get('age')),
                sex: parseInt(formData.get('sex')),
                cp: parseInt(formData.get('cp')),
                trestbps: parseFloat(formData.get('trestbps')),
                chol: parseFloat(formData.get('chol')),
                fbs: parseInt(formData.get('fbs')),
                restecg: parseInt(formData.get('restecg')),
                thalach: parseFloat(formData.get('thalach')),
                exang: parseInt(formData.get('exang')),
                oldpeak: parseFloat(formData.get('oldpeak')),
                slope: parseInt(formData.get('slope')),
                ca: parseInt(formData.get('ca')),
                thal: parseInt(formData.get('thal'))
            };

            const resultDiv = document.getElementById('heartResult');
            resultDiv.innerHTML = '<div class="alert alert-info">⏳ Predicting...</div>';

            try {
                const response = await apiFetch('/ml/predict/heart', {
                    method: 'POST',
                    body: JSON.stringify(features)
                });
                renderHeartResult(resultDiv, response);
            } catch (err) {
                resultDiv.innerHTML = `<div class="alert alert-danger">❌ Error: ${err.message}</div>`;
            }
        });
    }
});

function renderDiabetesResult(container, data) {
    const prediction = data.prediction;
    const probability = (data.probability * 100).toFixed(1);
    let alertClass, icon, message;

    if (prediction === 1) {
        alertClass = 'alert-danger';
        icon = '⚠️';
        message = `High risk of diabetes (probability: ${probability}%)`;
    } else {
        alertClass = 'alert-success';
        icon = '✅';
        message = `Low risk of diabetes (probability: ${probability}%)`;
    }

    container.innerHTML = `
        <div class="alert ${alertClass} d-flex align-items-center">
            <div class="me-2 fs-3">${icon}</div>
            <div>
                <strong>${data.message}</strong><br>
                ${message}<br>
                <small class="text-muted">Model confidence: ${probability}%</small>
            </div>
        </div>
    `;
}

function renderHeartResult(container, data) {
    const prediction = data.prediction;
    const probability = (data.probability * 100).toFixed(1);
    let alertClass, icon, message;

    if (prediction === 1) {
        alertClass = 'alert-danger';
        icon = '❤️‍🩹';
        message = `High risk of heart disease (probability: ${probability}%)`;
    } else {
        alertClass = 'alert-success';
        icon = '💚';
        message = `Low risk of heart disease (probability: ${probability}%)`;
    }

    container.innerHTML = `
        <div class="alert ${alertClass} d-flex align-items-center">
            <div class="me-2 fs-3">${icon}</div>
            <div>
                <strong>${data.message}</strong><br>
                ${message}<br>
                <small class="text-muted">Model confidence: ${probability}%</small>
            </div>
        </div>
    `;
}