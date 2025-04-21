document.addEventListener('DOMContentLoaded', () => {
  // ==================== CONFIGURAÇÕES ====================
  const config = {
      cardWidth: 320,        // Largura padrão do card em pixels
      cardGap: 40,           // Espaço entre os cards
      transitionTime: 400,   // Duração da animação em ms
      easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)', // Curva de animação
      debug: true,           // Modo debug
      viewportPadding: 20
  };

  // ==================== ESTADO ====================
  const state = {
      currentIndex: 0,       // Índice do card atual
      totalCards: 0,         // Total de cards visíveis
      cards: [],             // Array de elementos card
      isAnimating: false,    // Flag para evitar cliques durante animação
      filteredSubjects: [],  // IDs das disciplinas filtradas
      filteredDifficulties: [], // IDs das dificuldades filtradas
      carousel: null,        // Elemento do carrossel
      resizeTimer: null      // Timer para debounce do resize
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
      
      // Obter elementos do DOM
      state.carousel = document.querySelector(selectors.carousel);
      if (!state.carousel) {
          console.error('Elemento do carrossel não encontrado');
          return;
      }
      
      // Inicializar cards
      refreshCards();
      
      // Configurar eventos
      setupEventListeners();
      
      // Posicionar cards inicialmente
      setTimeout(() => {
          updateCarouselState();
          updatePagination();
          updateNavigationButtons();
      }, 100);
  }

  // ==================== GERENCIAMENTO DE CARDS ====================
  function refreshCards() {
      // Buscar todos os cards e filtrar os visíveis
      const allCards = document.querySelectorAll(selectors.cards);
      state.cards = Array.from(allCards);
      
      // Aplicar visibilidade com base nos filtros
      applyFilters();
      
      // Atualizar total de cards visíveis
      state.totalCards = state.cards.filter(card => !card.classList.contains('hidden')).length;
      
      // Reset para o primeiro card se necessário
      if (state.currentIndex >= state.totalCards) {
          state.currentIndex = Math.max(0, state.totalCards - 1);
      }
      
      logDebug(`Cards atualizados: ${state.totalCards} visíveis`);
      
      // Se não houver cards, mostrar estado vazio
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
          
          // Verificar se o card atende aos filtros ativos
          const matchesSubject = state.filteredSubjects.length === 0 || 
                                 state.filteredSubjects.includes(cardSubject);
          
          const matchesDifficulty = state.filteredDifficulties.length === 0 || 
                                     state.filteredDifficulties.includes(cardDifficulty);
          
          // Aplicar visibilidade
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
      // Verificar se já existe estado vazio
      let emptyState = document.querySelector('.empty-state');
      
      // Criar se não existir
      if (!emptyState) {
          emptyState = document.createElement('div');
          emptyState.className = 'empty-state';
          emptyState.innerHTML = `
              <span class="material-symbols-outlined">style</span>
              <p>Nenhum flashcard encontrado com os filtros selecionados.</p>
          `;
          state.carousel.appendChild(emptyState);
      }
      
      // Mostrar estado vazio
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
    
    // Definir a largura do card e calcular a posição
    const cardWidth = config.cardWidth;
    const gap = config.cardGap;
    const newPosition = -(state.currentIndex * (cardWidth + gap));
  
    // Aplica a transformação ao carrossel para centralizar o card atual
    state.carousel.style.transform = `translateX(${newPosition}px)`;
    
    // Atualiza classes e z-index de todos os cards
    visibleCards.forEach((card, index) => {
        // Primeiro, remover todas as classes de posição
        card.classList.remove('active', 'prev', 'next');
        
        // Não alterar o z-index se o cartão estiver em animação de flip
        if (!card.dataset.originalZIndex) {
            // Definir o z-index com base na distância do card atual
            const distance = Math.abs(index - state.currentIndex);
            // Cards mais próximos do atual têm z-index mais alto
            card.style.zIndex = 10 - distance;
        }
        
        // Aplicar classes de posição
        if (index === state.currentIndex) {
            card.classList.add('active');
        } else if (index === state.currentIndex - 1) {
            card.classList.add('prev');
        } else if (index === state.currentIndex + 1) {
            card.classList.add('next');
        }
    });

    // Logs de depuração
    logDebug('Cards visíveis: ' + visibleCards.length);
    logDebug('Posição calculada: ' + newPosition);
    logDebug('Largura do card: ' + cardWidth);

    // Atualizar navegação e paginação
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
      
      // Validar índice
      if (index < 0 || index >= visibleCards.length) {
          return;
      }
      
      // Atualizar índice e renderizar
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
      // Botões de navegação
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
      
      // Eventos de clique nos cards para flip
      state.cards.forEach(card => {
          const inner = card.querySelector('.flashcard-inner');
          if (inner) {
              inner.addEventListener('click', (e) => {
                  // Impedir flip durante animação do carrossel
                  if (state.isAnimating) return;
                  
                  // Verificar se este é o card ativo
                  const isActive = card.classList.contains('active');
                  
                  // Permitir virar apenas o card ativo
                  if (isActive) {
                      // Armazenar o z-index original antes de alterar
                      card.dataset.originalZIndex = card.style.zIndex;
                      // Trazer este card para frente durante a animação de flip
                      card.style.zIndex = "100";
                      inner.classList.toggle('flipped');
                  } else {
                      // Se clicar em um card não ativo, vamos navegar até ele
                      const cardIndex = state.cards.filter(c => !c.classList.contains('hidden')).indexOf(card);
                      if (cardIndex >= 0) {
                          navigateTo(cardIndex);
                      }
                  }
              });
          }
      });
      
      // Adicionar evento para o final da animação de flip
      state.cards.forEach(card => {
          const inner = card.querySelector('.flashcard-inner');
          if (inner) {
              inner.addEventListener('transitionend', (e) => {
                  // Se a transição foi de transformação (flip)
                  if (e.propertyName === 'transform') {
                      // Restaurar o z-index original após a animação de flip
                      if (card.dataset.originalZIndex) {
                          card.style.zIndex = card.dataset.originalZIndex;
                          delete card.dataset.originalZIndex;
                      }
                  }
              });
          }
      });
      
      // Chips de filtro rápido (dificuldade)
      const filterChips = document.querySelectorAll(selectors.chips.filter);
      filterChips.forEach(chip => {
          chip.addEventListener('click', () => {
              // Remover seleção de todos os chips de filtro
              filterChips.forEach(c => c.classList.remove('selected'));
              
              // Aplicar filtro de dificuldade
              const difficulty = chip.getAttribute('data-difficulty');
              
              if (difficulty === 'all') {
                  // Resetar filtro
                  state.filteredDifficulties = [];
              } else {
                  // Aplicar filtro específico
                  state.filteredDifficulties = [difficulty];
                  chip.classList.add('selected');
              }
              
              // Atualizar cards e carrossel
              refreshCards();
              state.currentIndex = 0;
              updateCarouselState();
          });
      });
      
      // Chips de disciplina
      const subjectChips = document.querySelectorAll(selectors.chips.subject);
      subjectChips.forEach(chip => {
          chip.addEventListener('click', () => {
              // Toggle seleção
              chip.classList.toggle('selected');
              
              // Atualizar array de disciplinas filtradas
              const subjectId = chip.getAttribute('data-id');
              if (chip.classList.contains('selected')) {
                  // Adicionar à lista de filtros
                  if (!state.filteredSubjects.includes(subjectId)) {
                      state.filteredSubjects.push(subjectId);
                  }
              } else {
                  // Remover da lista de filtros
                  state.filteredSubjects = state.filteredSubjects.filter(id => id !== subjectId);
              }
              
              // Não aplicar os filtros imediatamente, aguardar o botão "Iniciar revisão"
          });
      });
      
      // Chips de dificuldade
      const difficultyChips = document.querySelectorAll(selectors.chips.difficulty);
      difficultyChips.forEach(chip => {
          chip.addEventListener('click', () => {
              // Toggle seleção
              chip.classList.toggle('selected');
              
              // Atualizar array de dificuldades para filtro personalizado
              const difficultyId = chip.getAttribute('data-id');
              if (chip.classList.contains('selected')) {
                  // Adicionar à lista de filtros
                  if (!state.filteredDifficulties.includes(difficultyId)) {
                      state.filteredDifficulties.push(difficultyId);
                  }
              } else {
                  // Remover da lista de filtros
                  state.filteredDifficulties = state.filteredDifficulties.filter(id => id !== difficultyId);
              }
              
              // Não aplicar os filtros imediatamente, aguardar o botão "Iniciar revisão"
          });
      });
      
      // Botão iniciar revisão
      const startButton = document.querySelector(selectors.startButton);
      if (startButton) {
          startButton.addEventListener('click', () => {
              // Aplicar filtros selecionados
              refreshCards();
              state.currentIndex = 0;
              updateCarouselState();
              
              // Scroll para o carrossel
              const carousel = document.querySelector('.carousel-container');
              if (carousel) {
                  carousel.scrollIntoView({ behavior: 'smooth' });
              }
          });
      }
      
      // Redimensionamento da janela
      window.addEventListener('resize', () => {
          // Debounce para evitar múltiplas chamadas
          clearTimeout(state.resizeTimer);
          state.resizeTimer = setTimeout(() => {
              updateCarouselState();
          }, 200);
      });
      
      // Teclas de navegação
      document.addEventListener('keydown', (e) => {
          if (e.key === 'ArrowLeft') {
              navigatePrev();
          } else if (e.key === 'ArrowRight') {
              navigateNext();
          } else if (e.key === ' ' || e.key === 'Spacebar') {
              // Virar o card atual
              const visibleCards = state.cards.filter(card => !card.classList.contains('hidden'));
              const activeCard = visibleCards[state.currentIndex];
              if (activeCard) {
                  const inner = activeCard.querySelector('.flashcard-inner');
                  if (inner) {
                      // Armazenar o z-index original antes de alterar
                      activeCard.dataset.originalZIndex = activeCard.style.zIndex;
                      // Trazer este card para frente durante a animação de flip
                      activeCard.style.zIndex = "100";
                      inner.classList.toggle('flipped');
                  }
              }
              
              // Prevenir scroll
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

  // Inicialização
  init();
});