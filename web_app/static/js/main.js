// main.js — global utilities

// Highlight active nav link
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.href === window.location.href) a.classList.add('active');
});
