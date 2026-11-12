// PathWise Main JavaScript utilities

document.addEventListener('DOMContentLoaded', function () {
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 6000);
    });

    // Setup save career button listeners
    const saveButtons = document.querySelectorAll('.btn-save-career');
    saveButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const careerId = this.getAttribute('data-career-id');
            const icon = this.querySelector('i');
            const text = this.querySelector('.btn-text');

            fetch('/api/save-career', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ career_id: careerId })
            })
            .then(res => {
                if (res.status === 401) {
                    window.location.href = '/login';
                    return null;
                }
                return res.json();
            })
            .then(data => {
                if (!data) return;
                if (data.status === 'success') {
                    if (data.is_saved) {
                        if (icon) {
                            icon.classList.remove('bi-bookmark');
                            icon.classList.add('bi-bookmark-check-fill', 'text-warning');
                        }
                        if (text) text.textContent = 'Saved';
                        showToast('Career saved to your personal dashboard!');
                    } else {
                        if (icon) {
                            icon.classList.remove('bi-bookmark-check-fill', 'text-warning');
                            icon.classList.add('bi-bookmark');
                        }
                        if (text) text.textContent = 'Save';
                        showToast('Career removed from saved list.');
                    }
                }
            })
            .catch(err => console.error("Error saving career:", err));
        });
    });
});

// Toast notification helper
function showToast(message, type = 'info') {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
        toastContainer.style.zIndex = '1090';
        document.body.appendChild(toastContainer);
    }

    const toastEl = document.createElement('div');
    toastEl.className = 'toast align-items-center text-white bg-dark border-0 show shadow';
    toastEl.setAttribute('role', 'alert');
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body"><i class="bi bi-info-circle-fill text-info me-2"></i> ${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    toastContainer.appendChild(toastEl);
    setTimeout(() => {
        toastEl.remove();
    }, 4000);
}
