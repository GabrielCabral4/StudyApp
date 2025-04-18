document.addEventListener('DOMContentLoaded', function () {
    // Menu toggle responsivo (mantido do seu código original)
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
  
    // Implementação robusta para o carrossel centralizado
    function initCarousel() {
        const flashcards = document.querySelectorAll('.flashcard-item');
        const totalFlashcards = flashcards.length;
        
        if (totalFlashcards === 0) return; // Sair se não houver flashcards
        
        let currentIndex = 0;
        const carousel = document.querySelector('#flashcard-carousel');
        const carouselWrapper = document.querySelector('.carousel-wrapper');
        const cardWidth = 300; // Largura de cada flashcard
        const cardGap = 20;    // Espaçamento entre cards
        
        // Função para centralizar perfeitamente o card atual
        function centerCard() {
            // Remover classe active de todos os cards
            flashcards.forEach(card => card.classList.remove('active'));
            
            // Adicionar classe active ao card atual
            flashcards[currentIndex].classList.add('active');
            
            // Calcular o centro da tela
            const wrapperWidth = carouselWrapper.offsetWidth;
            const halfWrapperWidth = wrapperWidth / 2;
            
            // Calcular a posição do card atual no carrossel sem transformação
            const cardPosition = currentIndex * (cardWidth + cardGap);
            
            // Calcular quanto precisamos deslocar para centralizar exatamente este card
            const centerOffset = halfWrapperWidth - (cardWidth / 2);
            const translateAmount = cardPosition - centerOffset;
            
            // Aplicar a transformação precisa
            carousel.style.transform = `translateX(-${translateAmount}px)`;
        }
        
        // Configurar botões de navegação
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        
        if (btnPrev) {
            btnPrev.addEventListener('click', function() {
                currentIndex = (currentIndex - 1 + totalFlashcards) % totalFlashcards;
                centerCard();
            });
        }
        
        if (btnNext) {
            btnNext.addEventListener('click', function() {
                currentIndex = (currentIndex + 1) % totalFlashcards;
                centerCard();
            });
        }
        
        // Para garantir que a centralização aconteça assim que tudo estiver carregado
        window.addEventListener('load', centerCard);
        
        // Também centralizar logo após a inicialização do DOM
        centerCard();
        
        // E uma última tentativa após um pequeno atraso, caso algo ainda esteja sendo carregado
        setTimeout(centerCard, 200);
        
        // Ajustar ao redimensionar a janela
        window.addEventListener('resize', centerCard);
    }
    
    // Inicializar o carrossel
    initCarousel();
});