// ══════════════════════════════════════════════════════════════════════
// LearnLoop — JavaScript
// ══════════════════════════════════════════════════════════════════════

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.3s ease';
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  // Auto-scroll chat to bottom
  const chatWindow = document.querySelector('.chat-window');
  if (chatWindow) {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // Add smooth scroll behavior
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
});

// Chat message sending (for group detail page)
function sendChatMessage(event, groupId) {
  if (event.key === 'Enter' || event.type === 'click') {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (message) {
      // Submit the form
      document.getElementById('chatForm').submit();
    }
  }
}

// File upload preview
function previewFileName(input) {
  const fileName = input.files[0]?.name;
  if (fileName) {
    const label = input.nextElementSibling;
    if (label) {
      label.textContent = `📎 ${fileName}`;
    }
  }
}

// Confirm before leaving group
function confirmLeaveGroup() {
  return confirm('Are you sure you want to leave this group?');
}

// Search/filter functionality
function filterItems(searchInput, itemsSelector) {
  const query = searchInput.value.toLowerCase();
  const items = document.querySelectorAll(itemsSelector);
  
  items.forEach(item => {
    const text = item.textContent.toLowerCase();
    item.style.display = text.includes(query) ? '' : 'none';
  });
}

// Add animation class on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// Observe cards for animation
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.card, .feature-card, .student-card, .group-card');
  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });
});

// Form validation helper
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return true;
  
  const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
  let isValid = true;
  
  inputs.forEach(input => {
    if (!input.value.trim()) {
      input.style.borderColor = 'var(--red)';
      isValid = false;
    } else {
      input.style.borderColor = '';
    }
  });
  
  return isValid;
}

// Add active class to current nav link
document.addEventListener('DOMContentLoaded', () => {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});

console.log('📚 LearnLoop loaded successfully!');
