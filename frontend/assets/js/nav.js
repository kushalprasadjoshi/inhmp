// nav.js – inject role‑based navigation
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    const navContainer = document.querySelector('nav .navbar-nav');
    if (!navContainer) return;

    if (!token) {
        // Public nav
        navContainer.innerHTML = `
            <li class="nav-item"><a class="nav-link" href="/pages/login.html">Login</a></li>
            <li class="nav-item"><a class="nav-link" href="/pages/register.html">Register</a></li>
            <li class="nav-item"><a class="nav-link" href="/pages/ml_demo.html">Our Models</a></li>
        `;
        return;
    }

    // Decode token to get role
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const role = payload.role;

        let navItems = '';

        // Common for all authenticated users
        navItems += `<li class="nav-item"><span class="nav-link text-white-50">👤 ${payload.email}</span></li>`;

        // Role‑specific links
        if (role === 'Patient') {
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/patient_profile.html">Profile</a></li>`;
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/consent_grant.html">Grant Consent</a></li>`;
        }
        if (role === 'Doctor') {
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/visit_entry.html">New Visit</a></li>`;
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/consent_grant.html">Request Consent</a></li>`;
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/search_patient.html">Search Patient</a></li>`;
        }
        if (role === 'HospitalAdmin') {
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/hospital_dashboard.html">Hospitals</a></li>`;
        }
        if (role === 'EmergencyOfficer') {
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/emergency_override.html">Emergency</a></li>`;
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/analytics_dashboard.html">Analytics</a></li>`;
        }
        if (role === 'SystemAdmin') {
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/audit_logs.html">Audit Logs</a></li>`;
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/analytics_dashboard.html">Analytics</a></li>`;
            navItems += `<li class="nav-item"><a class="nav-link" href="/pages/hospital_dashboard.html">Hospitals</a></li>`;
        }

        // Always show AI models and logout
        navItems += `<li class="nav-item"><a class="nav-link" href="/pages/ml_demo.html">Our Models</a></li>`;
        navItems += `<li class="nav-item"><a class="nav-link" href="#" id="logoutBtnNav">Logout</a></li>`;

        navContainer.innerHTML = navItems;

        // Attach logout handler
        document.getElementById('logoutBtnNav')?.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('access_token');
            window.location.href = '/';
        });
    } catch (e) {
        console.error('Nav error', e);
    }
});