const API_GATEWAY_URL = 'YOUR_API_GATEWAY_URL_HERE';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');

    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Get form values
            const formData = {
                firstName: document.getElementById('firstName').value,
                lastName: document.getElementById('lastName').value,
                email: document.getElementById('email').value,
                countryCode: document.getElementById('countryCode').value,
                phoneNumber: document.getElementById('phoneNumber').value,
                message: document.getElementById('message').value
            };

            // Show loading state
            const submitButton = form.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting';

            try {
                const response = await fetch(API_GATEWAY_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    submitButton.textContent = 'Submitted';
                    form.reset();
                } else {
                    throw new Error(data.message || 'Submission failed');
                }
            } catch (error) {
                submitButton.textContent = 'Submission Failed';
            } finally {
                submitButton.disabled = false;
                setTimeout(() => {
                    submitButton.textContent = originalButtonText;
                }, 2000);
            }
        });
    }
});
