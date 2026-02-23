/* ══════════════════════════════════════════════════════════════════════
   Profile Picture Management with Crop & Edit
   ══════════════════════════════════════════════════════════════════════ */

let cropper = null;
let currentImage = null;

// ── Open Profile Picture Modal ──
function openProfilePictureModal() {
  const modal = document.getElementById('profilePictureModal');
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

// ── Close Profile Picture Modal ──
function closeProfilePictureModal() {
  const modal = document.getElementById('profilePictureModal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }
  
  // Destroy cropper if exists
  if (cropper) {
    cropper.destroy();
    cropper = null;
  }
  
  // Reset preview
  const preview = document.getElementById('imagePreview');
  if (preview) {
    preview.innerHTML = '<p style="color: #9CA3AF;">Select an image to preview</p>';
  }
}

// ── Trigger File Input ──
function triggerFileInput() {
  document.getElementById('profilePictureInput').click();
}

// ── Handle File Selection ──
function handleFileSelect(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  // Validate file type
  if (!file.type.match('image.*')) {
    showNotification('Please select an image file', 'error');
    return;
  }
  
  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    showNotification('Image size must be less than 5MB', 'error');
    return;
  }
  
  // Read and display image
  const reader = new FileReader();
  reader.onload = function(e) {
    currentImage = e.target.result;
    displayImageForCrop(currentImage);
  };
  reader.readAsDataURL(file);
}

// ── Display Image for Cropping ──
function displayImageForCrop(imageSrc) {
  const preview = document.getElementById('imagePreview');
  preview.innerHTML = `<img id="cropImage" src="${imageSrc}" style="max-width: 100%; display: block;">`;
  
  // Show crop controls
  document.getElementById('cropControls').style.display = 'block';
  
  // Initialize Cropper.js
  const image = document.getElementById('cropImage');
  cropper = new Cropper(image, {
    aspectRatio: 1,
    viewMode: 1,
    dragMode: 'move',
    autoCropArea: 1,
    restore: false,
    guides: true,
    center: true,
    highlight: false,
    cropBoxMovable: true,
    cropBoxResizable: true,
    toggleDragModeOnDblclick: false,
  });
}

// ── Crop Actions ──
function zoomIn() {
  if (cropper) cropper.zoom(0.1);
}

function zoomOut() {
  if (cropper) cropper.zoom(-0.1);
}

function rotateLeft() {
  if (cropper) cropper.rotate(-90);
}

function rotateRight() {
  if (cropper) cropper.rotate(90);
}

function flipHorizontal() {
  if (cropper) {
    const data = cropper.getData();
    cropper.scaleX(data.scaleX === 1 ? -1 : 1);
  }
}

function flipVertical() {
  if (cropper) {
    const data = cropper.getData();
    cropper.scaleY(data.scaleY === 1 ? -1 : 1);
  }
}

function resetCrop() {
  if (cropper) cropper.reset();
}

// ── Upload Cropped Image ──
function uploadCroppedImage() {
  if (!cropper) {
    showNotification('Please select an image first', 'error');
    return;
  }
  
  // Show loading
  const uploadBtn = document.getElementById('uploadBtn');
  const originalText = uploadBtn.innerHTML;
  uploadBtn.innerHTML = '<span class="spinner"></span> Uploading...';
  uploadBtn.disabled = true;
  
  // Get cropped canvas
  const canvas = cropper.getCroppedCanvas({
    width: 400,
    height: 400,
    imageSmoothingEnabled: true,
    imageSmoothingQuality: 'high',
  });
  
  // Convert to blob
  canvas.toBlob(function(blob) {
    const formData = new FormData();
    formData.append('profile_picture', blob, 'profile.jpg');
    
    // Upload via fetch
    fetch('/upload-profile-picture', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showNotification('Profile picture updated successfully!', 'success');
        
        // Update all profile pictures on page
        updateProfilePictures(data.profile_picture_url);
        
        // Close modal
        closeProfilePictureModal();
      } else {
        showNotification(data.error || 'Upload failed', 'error');
      }
    })
    .catch(error => {
      console.error('Upload error:', error);
      showNotification('Upload failed. Please try again.', 'error');
    })
    .finally(() => {
      uploadBtn.innerHTML = originalText;
      uploadBtn.disabled = false;
    });
  }, 'image/jpeg', 0.9);
}

// ── Remove Profile Picture ──
function removeProfilePicture() {
  if (!confirm('Are you sure you want to remove your profile picture?')) {
    return;
  }
  
  fetch('/remove-profile-picture', {
    method: 'POST'
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      showNotification('Profile picture removed', 'success');
      
      // Update all profile pictures to show initials
      updateProfilePictures(null);
      
      // Close modal
      closeProfilePictureModal();
    } else {
      showNotification(data.error || 'Failed to remove picture', 'error');
    }
  })
  .catch(error => {
    console.error('Remove error:', error);
    showNotification('Failed to remove picture', 'error');
  });
}

// ── Update Profile Pictures on Page ──
function updateProfilePictures(imageUrl) {
  // Update navbar profile button
  const profileBtn = document.querySelector('.profile-btn');
  if (profileBtn) {
    const avatar = profileBtn.querySelector('.profile-avatar');
    if (avatar) {
      if (imageUrl) {
        avatar.style.backgroundImage = `url(${imageUrl})`;
        avatar.style.backgroundSize = 'cover';
        avatar.style.backgroundPosition = 'center';
        avatar.textContent = '';
      } else {
        avatar.style.backgroundImage = 'none';
        const userName = profileBtn.querySelector('span').textContent;
        avatar.textContent = userName.charAt(0).toUpperCase();
      }
    }
  }
  
  // Update profile page image if exists
  const profileImage = document.getElementById('currentProfilePicture');
  if (profileImage) {
    if (imageUrl) {
      profileImage.src = imageUrl;
      profileImage.style.display = 'block';
    } else {
      profileImage.style.display = 'none';
    }
  }
  
  // Reload page to update all instances
  setTimeout(() => {
    window.location.reload();
  }, 1000);
}

// ── Show Notification ──
function showNotification(message, type = 'info') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <span class="notification-icon">${type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ'}</span>
    <span class="notification-message">${message}</span>
  `;
  
  // Add to page
  document.body.appendChild(notification);
  
  // Animate in
  setTimeout(() => notification.classList.add('show'), 10);
  
  // Remove after 3 seconds
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// ── Initialize ──
document.addEventListener('DOMContentLoaded', function() {
  // Add click handler to profile avatar
  const profileAvatar = document.querySelector('.profile-avatar');
  if (profileAvatar) {
    profileAvatar.style.cursor = 'pointer';
    profileAvatar.addEventListener('click', function(e) {
      e.stopPropagation();
      openProfilePictureModal();
    });
  }
  
  // Close modal on outside click
  const modal = document.getElementById('profilePictureModal');
  if (modal) {
    modal.addEventListener('click', function(e) {
      if (e.target === modal) {
        closeProfilePictureModal();
      }
    });
  }
  
  // File input change handler
  const fileInput = document.getElementById('profilePictureInput');
  if (fileInput) {
    fileInput.addEventListener('change', handleFileSelect);
  }
  
  // Keyboard shortcuts
  document.addEventListener('keydown', function(e) {
    if (modal && modal.style.display === 'flex') {
      if (e.key === 'Escape') {
        closeProfilePictureModal();
      }
    }
  });
});

// ── Drag and Drop Support ──
document.addEventListener('DOMContentLoaded', function() {
  const preview = document.getElementById('imagePreview');
  if (!preview) return;
  
  preview.addEventListener('dragover', function(e) {
    e.preventDefault();
    this.style.borderColor = '#2563EB';
    this.style.background = 'rgba(37, 99, 235, 0.05)';
  });
  
  preview.addEventListener('dragleave', function(e) {
    e.preventDefault();
    this.style.borderColor = '#E5E7EB';
    this.style.background = 'white';
  });
  
  preview.addEventListener('drop', function(e) {
    e.preventDefault();
    this.style.borderColor = '#E5E7EB';
    this.style.background = 'white';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.match('image.*')) {
      const reader = new FileReader();
      reader.onload = function(event) {
        currentImage = event.target.result;
        displayImageForCrop(currentImage);
      };
      reader.readAsDataURL(file);
    }
  });
});
