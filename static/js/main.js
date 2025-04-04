document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Show loading state
                const submitBtn = form.querySelector('#submitBtn');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    const spinner = submitBtn.querySelector('.spinner-border');
                    if (spinner) {
                        spinner.classList.remove('d-none');
                    }
                }
            }
            
            form.classList.add('was-validated');
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Character counter for textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            const maxLength = this.getAttribute('maxlength');
            if (maxLength) {
                const counter = this.parentElement.querySelector('.char-counter');
                if (counter) {
                    counter.textContent = `${this.value.length}/${maxLength}`;
                }
            }
        });
    });

    // Smooth scroll for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});
