const API_GATEWAY_URL = 'YOUR_API_GATEWAY_URL_HERE';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const aboutNav = document.getElementById('aboutNav');
    const enquiriesNav = document.getElementById('enquiriesNav');
    const aboutCard = document.querySelector('.section.about');
    const investedCard = document.querySelector('.section.hover');
    const contactCard = document.querySelector('.section.contact');

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

    // Helper to play the push + bounce animation on a card
    function playCardAnimation(card) {
        if (!card) return;
        card.classList.remove('card-animate-bounce');
        // Force reflow so animation restarts
        // eslint-disable-next-line no-void
        void card.offsetWidth;
        card.classList.add('card-animate-bounce');
    }

    // About: first READY FOR SOME SUM, then £20K INVESTED
    if (aboutNav) {
        aboutNav.addEventListener('click', function(e) {
            e.preventDefault();
            if (!aboutCard || !investedCard) return;

            playCardAnimation(aboutCard);

            aboutCard.addEventListener(
                'animationend',
                function handler() {
                    aboutCard.removeEventListener('animationend', handler);
                    playCardAnimation(investedCard);
                }
            );
        });
    }

    // Enquiries: CONTACT US DIRECT card
    if (enquiriesNav) {
        enquiriesNav.addEventListener('click', function(e) {
            e.preventDefault();
            if (!contactCard) return;
            playCardAnimation(contactCard);
        });
    }
});
