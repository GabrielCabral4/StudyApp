document.addEventListener('DOMContentLoaded', function () {
    // 🟦 Menu toggle responsivo
    const menuToggle = document.createElement('div');
    menuToggle.classList.add('menu-toggle');
    menuToggle.innerHTML = 'menu';
    document.body.appendChild(menuToggle);
  
    menuToggle.addEventListener('click', function () {
      document.querySelector('.sidebar').classList.toggle('active');
      document.querySelector('.content').classList.toggle('pushed');
    });
  
    if (window.innerWidth <= 768) {
      const menuItems = document.querySelectorAll('.menu-content li a');
      menuItems.forEach(item => {
        item.addEventListener('click', function () {
          document.querySelector('.sidebar').classList.remove('active');
          document.querySelector('.content').classList.remove('pushed');
        });
      });
    }
  
    // Flashcard carousel functionality
    const flashcards = document.querySelectorAll('.flashcard-item');
    const totalFlashcards = flashcards.length;
    let currentIndex = 0;
    
    if (totalFlashcards > 0) {
        function updateCarousel() {
            // Remove active class from all flashcards
            flashcards.forEach((flashcard, index) => {
                flashcard.classList.remove('active');
                
                // Add active class to current flashcard
                if (index === currentIndex) {
                    flashcard.classList.add('active');
                }
            });
            
            // Calculate center position for the current card
            const carousel = document.querySelector('.flashcard-carousel');
            const carouselWidth = document.querySelector('.carousel-wrapper').offsetWidth;
            const cardWidth = 300; // Width of a flashcard
            const cardGap = 20; // Gap between cards
            
            // Calculate position to center the current card
            const centerOffset = (carouselWidth - cardWidth) / 2;
            const translateX = currentIndex * (cardWidth + cardGap) - centerOffset;
            
            // Apply transform with smooth transition
            carousel.style.transform = `translateX(-${translateX}px)`;
        }
        
        // Event listeners for next/prev buttons
        document.getElementById('btn-prev').addEventListener('click', function() {
            currentIndex = (currentIndex - 1 + totalFlashcards) % totalFlashcards;
            updateCarousel();
        });

        document.getElementById('btn-next').addEventListener('click', function() {
            currentIndex = (currentIndex + 1) % totalFlashcards;
            updateCarousel();
        });

        // Initialize carousel with centered first card
        window.addEventListener('load', function() {
            updateCarousel();
        });
        
        // Also handle window resize
        window.addEventListener('resize', function() {
            updateCarousel();
        });
        
        // Initialize carousel immediately
        updateCarousel();
    }
});