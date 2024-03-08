document.addEventListener("DOMContentLoaded", function() {
  var logoContainer = document.getElementById('logo-container');
  
  setTimeout(function() {
      logoContainer.style.animation = 'fadeOut 1s ease forwards';
      
      // Adjust opacity gradually to 40% after the animation finishes
      setTimeout(function() {
          logoContainer.style.animation = 'opacityToForty 1s ease forwards';
      }, 1000); // 1000 milliseconds = 1 second (duration of fadeOut animation)
  }, 4000); // 4000 milliseconds = 4 seconds
});
