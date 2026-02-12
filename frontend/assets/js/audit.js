document.addEventListener('DOMContentLoaded', async () => {
    try {
        const logs = await apiFetch('/audit/logs');
        const tableBody = document.querySelector('#auditTable tbody');
        tableBody.innerHTML = '';
        logs.forEach(log => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${new Date(log.timestamp).toLocaleString()}</td>
                <td>${log.user_id ? log.user_id.slice(0,8) : 'System'}</td>
                <td>${log.action}</td>
                <td>${log.resource_type || '-'}</td>
                <td>${log.resource_id ? log.resource_id.slice(0,8) : '-'}</td>
                <td>
                    ${log.old_value ? `<span class="badge bg-warning">Old</span>` : ''}
                    ${log.new_value ? `<span class="badge bg-info">New</span>` : ''}
                </td>
            `;
            tableBody.appendChild(row);
        });
        // Initialize DataTable
        $('#auditTable').DataTable({
            order: [[0, 'desc']],
            pageLength: 25
        });
    } catch (err) {
        alert('Failed to load audit logs: ' + err.message);
    }

    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/';
    });
});