// API Gateway endpoint URL - Replace this with your actual API Gateway URL after deployment
// You can get this from: terraform output api_gateway_url
const API_GATEWAY_URL = 'YOUR_API_GATEWAY_URL_HERE';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');

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
            submitButton.textContent = 'Submitting...';
            formMessage.style.display = 'none';

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
                    formMessage.style.display = 'block';
                    formMessage.style.color = 'green';
                    formMessage.textContent = 'Thank you! Your message has been submitted successfully.';
                    form.reset();
                } else {
                    throw new Error(data.message || 'Submission failed');
                }
            } catch (error) {
                formMessage.style.display = 'block';
                formMessage.style.color = 'red';
                formMessage.textContent = 'Error: ' + error.message + '. Please try again.';
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            }
        });
    }
});
