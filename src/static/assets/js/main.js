/* static/assets/js/main.js */

/* Hyperspace Core JavaScript */
window.onload = function() {
    document.body.classList.remove('is-preload');
  };
  
  /* Smooth scrolling for anchors */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
          e.preventDefault();
          document.querySelector(this.getAttribute('href')).scrollIntoView({
              behavior: 'smooth'
          });
      });
  });
  