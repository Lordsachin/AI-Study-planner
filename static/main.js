document.addEventListener('DOMContentLoaded', () => {
    // === Login/Register Logic ===
    const authForm = document.getElementById('auth-form');
    if (authForm) {
        let isLoginMode = true;
        const switchBtn = document.getElementById('switch-mode');
        const formTitle = document.getElementById('form-title');
        const submitBtn = document.getElementById('submit-btn');
        const promptTxt = document.getElementById('switch-prompt');
        const errorMsg = document.getElementById('error-msg');

        switchBtn.addEventListener('click', (e) => {
            e.preventDefault();
            isLoginMode = !isLoginMode;
            if (isLoginMode) {
                formTitle.innerText = "Welcome Back";
                submitBtn.innerText = "Login";
                promptTxt.innerText = "Don't have an account?";
                switchBtn.innerText = "Register here";
            } else {
                formTitle.innerText = "Create Account";
                submitBtn.innerText = "Register";
                promptTxt.innerText = "Already have an account?";
                switchBtn.innerText = "Login here";
            }
            errorMsg.innerText = "";
        });

        authForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            submitBtn.disabled = true;

            const endpoint = isLoginMode ? '/login' : '/register';
            try {
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                const data = await res.json();
                if (data.success) {
                    if (!isLoginMode) {
                        // Switch to login mode automatically
                        switchBtn.click();
                        errorMsg.style.color = '#10b981';
                        errorMsg.innerText = "Registration successful! You can now login.";
                        setTimeout(() => { errorMsg.style.color = '#f87171'; errorMsg.innerText = ''; }, 3000);
                    } else {
                        window.location.href = "/";
                    }
                } else {
                    errorMsg.innerText = data.message;
                }
            } catch (err) {
                errorMsg.innerText = "Something went wrong. Ensure server is running.";
            } finally {
                submitBtn.disabled = false;
            }
        });
    }

    // === Dashboard Logic ===
    const predictForm = document.getElementById('predict-form');
    if (predictForm) {
        let chartInstance = null;
        
        const loadRecords = async () => {
            try {
                const res = await fetch('/api/records');
                const data = await res.json();
                if (data.success) {
                    updateChart(data.records);
                    if(data.records.length > 0) {
                        updateLatestAI(data.records[data.records.length - 1]);
                    }
                }
            } catch(e) { console.error("Error loading records", e); }
        };

        const updateChart = (records) => {
            const ctx = document.getElementById('performanceChart').getContext('2d');
            const labels = records.map(r => r.subject_name);
            const predicted = records.map(r => r.predicted_score);
            const previous = records.map(r => r.previous_score);

            if (chartInstance) chartInstance.destroy();

            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        { label: 'Previous Score', data: previous, backgroundColor: 'rgba(148, 163, 184, 0.5)' },
                        { label: 'AI Predicted Score', data: predicted, backgroundColor: 'rgba(99, 102, 241, 0.8)' }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, max: 100, ticks: { color: '#94a3b8' } },
                        x: { ticks: { color: '#94a3b8' } }
                    },
                    plugins: {
                        legend: { labels: { color: '#f8fafc' } }
                    }
                }
            });
        };

        const updateLatestAI = (record) => {
            const container = document.getElementById('latest-ai');
            
            let suggestionHtml = record.suggestion;
            if (suggestionHtml.includes("WARNING:")) {
                let parts = suggestionHtml.split("WARNING:");
                suggestionHtml = parts[0] + `<div style="color: #fca5a5; font-weight: bold; margin-top: 12px; padding: 12px; border-radius: 8px; background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; font-size: 0.9em;">🚨 WARNING: ${parts[1]}</div>`;
            }

            container.innerHTML = `
                <div class="ai-card ${record.priority}">
                    <h4>${record.subject_name}</h4>
                    <div class="score">${record.predicted_score}% <span style="font-size:0.4em; color:#94a3b8; font-weight:normal;">Predicted Score</span></div>
                    <span class="priority ${record.priority}">Priority: ${record.priority}</span>
                    <p class="ai-suggestion">${suggestionHtml}</p>
                </div>
            `;
        };

        predictForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = predictForm.querySelector('button');
            const msg = document.getElementById('predict-msg');
            btn.disabled = true;
            msg.style.color = '#94a3b8';
            msg.innerText = "Analyzing...";

            const payload = {
                subject_name: document.getElementById('subject').value,
                study_hours_before: document.getElementById('hours_before').value,
                study_hours_after: document.getElementById('hours_after').value,
                attendance: document.getElementById('attendance').value,
                previous_score: document.getElementById('prev_score').value
            };

            try {
                const res = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.success) {
                    msg.style.color = '#10b981';
                    msg.innerText = "AI Plan Created!";
                    predictForm.reset();
                    loadRecords(); // Refresh data
                    setTimeout(() => msg.innerText='', 3000);
                } else {
                    msg.style.color = '#f87171';
                    msg.innerText = data.message || "Failed to predict.";
                }
            } catch(err) {
                msg.style.color = '#f87171';
                msg.innerText = "Server error.";
            } finally {
                btn.disabled = false;
            }
        });

        // Initial load
        loadRecords();
    }
});
