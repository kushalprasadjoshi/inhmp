document.addEventListener('DOMContentLoaded', async () => {
    await loadDiseaseChart();
    await loadTrendChart();
    await loadOutbreakAlerts();

    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/';
    });
});

async function loadDiseaseChart() {
    try {
        const data = await apiFetch('/analytics/disease-summary');
        const labels = data.map(d => `${d.district} - ${d.diagnosis_code}`);
        const values = data.map(d => d.cases);
        new Chart(document.getElementById('diseaseChart'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Cases',
                    data: values,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)'
                }]
            }
        });
    } catch (err) {
        console.error('Disease chart error', err);
    }
}

async function loadTrendChart() {
    try {
        const data = await apiFetch('/analytics/trends');
        const labels = data.map(d => `Week ${d.week}`);
        const values = data.map(d => d.cases);
        new Chart(document.getElementById('trendChart'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Respiratory Cases',
                    data: values,
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }]
            }
        });
    } catch (err) {
        console.error('Trend chart error', err);
    }
}

async function loadOutbreakAlerts() {
    try {
        const alerts = await apiFetch('/analytics/outbreak-alerts');
        const tbody = document.getElementById('outbreakTable');
        tbody.innerHTML = '';
        alerts.forEach(a => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${a.district}</td>
                <td>${a.date}</td>
                <td>${a.daily_cases}</td>
                <td>${a.avg_4day.toFixed(1)}</td>
                <td class="text-danger">+${(a.daily_cases - a.avg_4day).toFixed(1)}</td>
            `;
        });
    } catch (err) {
        console.error('Outbreak alerts error', err);
    }
}