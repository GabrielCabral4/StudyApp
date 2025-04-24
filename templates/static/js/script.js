document.addEventListener('DOMContentLoaded', () => {
  // ==================== CONFIGURAÇÕES ====================
  const config = {
      cardWidth: 320,        
      cardGap: 40,           
      transitionTime: 400,  
      easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
      debug: true,          
      viewportPadding: 20
  };

  // ==================== ESTADO ====================
  const state = {
      currentIndex: 0,       
      totalCards: 0,         
      cards: [],             
      isAnimating: false,
      filteredSubjects: [],  
      filteredDifficulties: [], 
      carousel: null,        
      resizeTimer: null      
  };

  // ==================== SELETORES DOM ====================
  const selectors = {
      carousel: '#flashcard-carousel',
      prevButton: '#prev-button',
      nextButton: '#next-button',
      cards: '.flashcard-item',
      chips: {
          filter: '.chip-filter',
          subject: '.chip-subject',
          difficulty: '.chip-difficulty'
      },
      startButton: '#start-review',
      pagination: {
          current: '.current-card',
          total: '.total-cards'
      }
  };

  // ==================== INICIALIZAÇÃO ====================
  function init() {
      logDebug('Inicializando carrossel de flashcards');
      
      state.carousel = document.querySelector(selectors.carousel);
      if (!state.carousel) {
          console.error('Elemento do carrossel não encontrado');
          return;
      }
      
      refreshCards();
      
      setupEventListeners();
      
      setTimeout(() => {
          updateCarouselState();
          updatePagination();
          updateNavigationButtons();
      }, 100);
  }

  // ==================== GERENCIAMENTO DE CARDS ====================
  function refreshCards() {
      const allCards = document.querySelectorAll(selectors.cards);
      state.cards = Array.from(allCards);
      
      applyFilters();
      
      state.totalCards = state.cards.filter(card => !card.classList.contains('hidden')).length;
      
      if (state.currentIndex >= state.totalCards) {
          state.currentIndex = Math.max(0, state.totalCards - 1);
      }
      
      logDebug(`Cards atualizados: ${state.totalCards} visíveis`);
      
      if (state.totalCards === 0) {
          showEmptyState();
      } else {
          hideEmptyState();
      }
  }

  function applyFilters() {
      state.cards.forEach(card => {
          const cardSubject = card.getAttribute('data-subject');
          const cardDifficulty = card.getAttribute('data-difficulty');
          
          const matchesSubject = state.filteredSubjects.length === 0 || 
                                 state.filteredSubjects.includes(cardSubject);
          
          const matchesDifficulty = state.filteredDifficulties.length === 0 || 
                                     state.filteredDifficulties.includes(cardDifficulty);
          
          if (matchesSubject && matchesDifficulty) {
              card.classList.remove('hidden');
              card.classList.add('visible');
          } else {
              card.classList.add('hidden');
              card.classList.remove('visible', 'active', 'prev', 'next');
          }
      });
  }
  
  function showEmptyState() {
      let emptyState = document.querySelector('.empty-state');
      
      if (!emptyState) {
          emptyState = document.createElement('div');
          emptyState.className = 'empty-state';
          emptyState.innerHTML = `
              <span class="material-symbols-outlined">style</span>
              <p>Nenhum flashcard encontrado com os filtros selecionados.</p>
          `;
          state.carousel.appendChild(emptyState);
      }
      
      emptyState.style.display = 'flex';
  }
  
  function hideEmptyState() {
      const emptyState = document.querySelector('.empty-state');
      if (emptyState) {
          emptyState.style.display = 'none';
      }
  }

  // ==================== NAVEGAÇÃO DO CARROSSEL ====================
  function updateCarouselState() {
    if (state.isAnimating) return;
    state.isAnimating = true;

    const visibleCards = state.cards.filter(card => !card.classList.contains('hidden'));
    
    if (visibleCards.length === 0) {
        state.isAnimating = false;
        return;
    }
    
    const cardWidth = config.cardWidth;
    const gap = config.cardGap;
    const newPosition = -(state.currentIndex * (cardWidth + gap));
  
    state.carousel.style.transform = `translateX(${newPosition}px)`;
    
    visibleCards.forEach((card, index) => {
        card.classList.remove('active', 'prev', 'next');
        
        if (!card.dataset.originalZIndex) {
            const distance = Math.abs(index - state.currentIndex);
            card.style.zIndex = 10 - distance;
        }
        
        if (index === state.currentIndex) {
            card.classList.add('active');
        } else if (index === state.currentIndex - 1) {
            card.classList.add('prev');
        } else if (index === state.currentIndex + 1) {
            card.classList.add('next');
        }
    });

    logDebug('Cards visíveis: ' + visibleCards.length);
    logDebug('Posição calculada: ' + newPosition);
    logDebug('Largura do card: ' + cardWidth);

    updateNavigationButtons();
    updatePagination();

    setTimeout(() => {
        state.isAnimating = false;
    }, config.transitionTime);
  }

  function updateNavigationButtons() {
      const visibleCards = state.cards.filter(card => !card.classList.contains('hidden'));
      const prevButton = document.querySelector(selectors.prevButton);
      const nextButton = document.querySelector(selectors.nextButton);
      
      if (prevButton) {
          prevButton.classList.toggle('disabled', state.currentIndex <= 0);
      }
      
      if (nextButton) {
          nextButton.classList.toggle('disabled', state.currentIndex >= visibleCards.length - 1);
      }
  }
  
  function updatePagination() {
      const visibleCards = state.cards.filter(card => !card.classList.contains('hidden'));
      const currentElement = document.querySelector(selectors.pagination.current);
      const totalElement = document.querySelector(selectors.pagination.total);
      
      if (currentElement) {
          currentElement.textContent = visibleCards.length > 0 ? state.currentIndex + 1 : 0;
      }
      
      if (totalElement) {
          totalElement.textContent = visibleCards.length;
      }
  }
  
  function navigateTo(index) {
      const visibleCards = state.cards.filter(card => !card.classList.contains('hidden'));
      
      if (index < 0 || index >= visibleCards.length) {
          return;
      }
      
      state.currentIndex = index;
      updateCarouselState();
  }
  
  function navigatePrev() {
      if (state.currentIndex > 0) {
          navigateTo(state.currentIndex - 1);
      }
  }
  
  function navigateNext() {
      const visibleCards = state.cards.filter(card => !card.classList.contains('hidden'));
      if (state.currentIndex < visibleCards.length - 1) {
          navigateTo(state.currentIndex + 1);
      }
  }

  // ==================== EVENTOS ====================
  function setupEventListeners() {
      const prevButton = document.querySelector(selectors.prevButton);
      const nextButton = document.querySelector(selectors.nextButton);
      
      if (prevButton) {
          prevButton.addEventListener('click', () => {
              navigatePrev();
          });
      }
      
      if (nextButton) {
          nextButton.addEventListener('click', () => {
              navigateNext();
          });
      }
      
      state.cards.forEach(card => {
          const inner = card.querySelector('.flashcard-inner');
          if (inner) {
              inner.addEventListener('click', (e) => {
                  if (state.isAnimating) return;
                  
                  const isActive = card.classList.contains('active');
                  
                  if (isActive) {
                      card.dataset.originalZIndex = card.style.zIndex;
                      card.style.zIndex = "100";
                      inner.classList.toggle('flipped');
                  } else {
                      const cardIndex = state.cards.filter(c => !c.classList.contains('hidden')).indexOf(card);
                      if (cardIndex >= 0) {
                          navigateTo(cardIndex);
                      }
                  }
              });
          }
      });
      
      state.cards.forEach(card => {
          const inner = card.querySelector('.flashcard-inner');
          if (inner) {
              inner.addEventListener('transitionend', (e) => {
                  if (e.propertyName === 'transform') {
                      if (card.dataset.originalZIndex) {
                          card.style.zIndex = card.dataset.originalZIndex;
                          delete card.dataset.originalZIndex;
                      }
                  }
              });
          }
      });
      
      const filterChips = document.querySelectorAll(selectors.chips.filter);
      filterChips.forEach(chip => {
          chip.addEventListener('click', () => {
              filterChips.forEach(c => c.classList.remove('selected'));
              
              const difficulty = chip.getAttribute('data-difficulty');
              
              if (difficulty === 'all') {
                  state.filteredDifficulties = [];
              } else {
                  state.filteredDifficulties = [difficulty];
                  chip.classList.add('selected');
              }
              
              refreshCards();
              state.currentIndex = 0;
              updateCarouselState();
          });
      });
      
      const subjectChips = document.querySelectorAll(selectors.chips.subject);
      subjectChips.forEach(chip => {
          chip.addEventListener('click', () => {
              chip.classList.toggle('selected');
              
              const subjectId = chip.getAttribute('data-id');
              if (chip.classList.contains('selected')) {
                  if (!state.filteredSubjects.includes(subjectId)) {
                      state.filteredSubjects.push(subjectId);
                  }
              } else {
                  state.filteredSubjects = state.filteredSubjects.filter(id => id !== subjectId);
              }
              
          });
      });
      
      const difficultyChips = document.querySelectorAll(selectors.chips.difficulty);
      difficultyChips.forEach(chip => {
          chip.addEventListener('click', () => {
              chip.classList.toggle('selected');
              
              const difficultyId = chip.getAttribute('data-id');
              if (chip.classList.contains('selected')) {
                  if (!state.filteredDifficulties.includes(difficultyId)) {
                      state.filteredDifficulties.push(difficultyId);
                  }
              } else {
                  state.filteredDifficulties = state.filteredDifficulties.filter(id => id !== difficultyId);
              }
              
          });
      });
      
      const startButton = document.querySelector(selectors.startButton);
      if (startButton) {
          startButton.addEventListener('click', () => {
              refreshCards();
              state.currentIndex = 0;
              updateCarouselState();
              
              const carousel = document.querySelector('.carousel-container');
              if (carousel) {
                  carousel.scrollIntoView({ behavior: 'smooth' });
              }
          });
      }
      
      window.addEventListener('resize', () => {
          clearTimeout(state.resizeTimer);
          state.resizeTimer = setTimeout(() => {
              updateCarouselState();
          }, 200);
      });
      
      document.addEventListener('keydown', (e) => {
          if (e.key === 'ArrowLeft') {
              navigatePrev();
          } else if (e.key === 'ArrowRight') {
              navigateNext();
          } else if (e.key === ' ' || e.key === 'Spacebar') {
              const visibleCards = state.cards.filter(card => !card.classList.contains('hidden'));
              const activeCard = visibleCards[state.currentIndex];
              if (activeCard) {
                  const inner = activeCard.querySelector('.flashcard-inner');
                  if (inner) {
                      activeCard.dataset.originalZIndex = activeCard.style.zIndex;
                      activeCard.style.zIndex = "100";
                      inner.classList.toggle('flipped');
                  }
              }
              
              e.preventDefault();
          }
      });
  }

  // ==================== UTILITÁRIOS ====================
  function logDebug(message) {
      if (config.debug) {
          console.log(`[Flashcards] ${message}`);
      }
  }

  init();
});