// Global js for eLearning Platform
(function () {
  'use strict';

  // Example: Smooth scroll for internal anchors
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const href = anchor.getAttribute('href');
      if (href && href.length > 1) {
        e.preventDefault();
        document.querySelector(href)?.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Auto-dismiss alerts after 5s
  const alerts = document.querySelectorAll('.alert[data-autoclose]');
  alerts.forEach((el) => setTimeout(() => el.classList.add('fade'), 4500));
})();
