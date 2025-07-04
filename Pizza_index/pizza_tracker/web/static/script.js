// pizza_tracker/web/static/script.js

// This script will fetch data from the API and update the UI.

async function fetchData() {
    const response = await fetch('/api/status');
    const data = await response.json();

    const statusIndicator = document.getElementById('status-indicator');
    if (data.status === 'abnormal') {
        statusIndicator.textContent = data.message || 'anomaly detected – danger likely';
        statusIndicator.className = 'anomaly';
    } else {
        statusIndicator.textContent = data.message || 'nominal busyness';
        statusIndicator.className = 'nominal';
    }
}

fetchData();
