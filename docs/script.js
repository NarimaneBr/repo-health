document.addEventListener('DOMContentLoaded', () => {

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.copy-btn');

    copyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                const textToCopy = targetElement.innerText;

                navigator.clipboard.writeText(textToCopy).then(() => {
                    // Visual feedback
                    const originalText = button.innerText;
                    button.innerText = 'Copied!';
                    button.classList.add('copied');

                    setTimeout(() => {
                        button.innerText = originalText;
                        button.classList.remove('copied');
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            }
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const id = this.getAttribute('href');
            if (id === '#') return;

            const target = document.querySelector(id);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
