/**
 * HSE Management System - Frontend Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('HSE System Initialized');

    // Simple fade-in for alert messages
    const alerts = document.querySelectorAll('.bg-green-100, .bg-red-50');
    alerts.forEach(alert => {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.5s ease-in-out';
        setTimeout(() => alert.style.opacity = '1', 100);
    });

    // Handle mobile sidebar toggle (if implemented)
    // Placeholder for chart initialization (ApexCharts/Chart.js)
});
