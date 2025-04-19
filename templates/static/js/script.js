document.addEventListener('DOMContentLoaded', () => {
  // ─── VARIÁVEIS GLOBAIS ──────────────────────────────────────────────────
  let quickActive = null;
  let currentCarouselCleanup = null;
  
  // ─── MENU TOGGLE ───────────────────────────────────────────────────────
  const menuToggle = document.createElement('div');
  menuToggle.classList.add('menu-toggle');
  menuToggle.innerHTML = 'menu';
  document.body.appendChild(menuToggle);

  menuToggle.addEventListener('click', () => {
    document.querySelector('.sidebar').classList.toggle('active');
    document.querySelector('.content').classList.toggle('pushed');
  });

  if (window.innerWidth <= 768) {
    document.querySelectorAll('.menu-content li a').forEach(a =>
      a.addEventListener('click', () => {
        document.querySelector('.sidebar').classList.remove('active');
        document.querySelector('.content').classList.remove('pushed');
      })
    );
  }

  // ─── CARROSSEL (VERSÃO CORRIGIDA) ──────────────────────────────────────
  function initCarousel() {
    if (currentCarouselCleanup) {
        currentCarouselCleanup();
    }

    const carousel = document.getElementById('flashcard-carousel');
    const wrapper = document.querySelector('.carousel-wrapper');
    const cards = Array.from(document.querySelectorAll('.flashcard-item.visivel'));
    const totalCards = cards.length;

    if (totalCards === 0) {
        carousel.style.transform = 'translateX(0)';
        return;
    }

    const cardWidth = cards[0].offsetWidth;
    const gap = parseInt(getComputedStyle(carousel).gap) || 20;
    let currentIndex = 0;
    let wrapperWidth = wrapper.offsetWidth;
    let initialOffset = (wrapperWidth - cardWidth) / 2;

    // Desativa temporariamente a transição para o posicionamento inicial
    carousel.style.transition = 'none';
    
    function updateCarousel() {
        currentIndex = Math.max(0, Math.min(currentIndex, totalCards - 1));
        const newPosition = -currentIndex * (cardWidth + gap) + initialOffset;
        
        carousel.style.transform = `translateX(${newPosition}px)`;
        
        cards.forEach((card, idx) => {
            card.classList.toggle('active', idx === currentIndex);
        });
        
        updateButtons();
    }

    function updateButtons() {
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        
        if (totalCards <= 1) {
            btnPrev?.classList.add('disabled');
            btnNext?.classList.add('disabled');
        } else {
            btnPrev?.classList.toggle('disabled', currentIndex === 0);
            btnNext?.classList.toggle('disabled', currentIndex >= totalCards - 1);
        }
    }

    function handlePrevClick() {
        if (currentIndex > 0) {
            currentIndex--;
            carousel.style.transition = 'transform 0.3s ease';
            updateCarousel();
        }
    }
    
    function handleNextClick() {
        if (currentIndex < totalCards - 1) {
            currentIndex++;
            carousel.style.transition = 'transform 0.3s ease';
            updateCarousel();
        }
    }

    function handleResize() {
        wrapperWidth = wrapper.offsetWidth;
        initialOffset = (wrapperWidth - cardWidth) / 2;
        carousel.style.transition = 'none';
        updateCarousel();
        setTimeout(() => {
            carousel.style.transition = 'transform 0.3s ease';
        }, 50);
    }

    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    btnPrev?.addEventListener('click', handlePrevClick);
    btnNext?.addEventListener('click', handleNextClick);

    window.addEventListener('resize', handleResize);

    // Posicionamento inicial sem animação
    updateCarousel();
    
    // Reativa a transição após um pequeno delay
    setTimeout(() => {
        carousel.style.transition = 'transform 0.3s ease';
    }, 50);

    currentCarouselCleanup = () => {
        btnPrev?.removeEventListener('click', handlePrevClick);
        btnNext?.removeEventListener('click', handleNextClick);
        window.removeEventListener('resize', handleResize);
    };
}

  // ─── QUICK FILTERS ────────────────────────────────────────────────────
  document.querySelectorAll('.chip-filtro').forEach(chip => {
    chip.addEventListener('click', () => {
      const lvl = chip.dataset.filtroDificuldade;
      
      if (quickActive === chip) {
        chip.classList.remove('selecionado');
        quickActive = null;
        document.querySelectorAll('.flashcard-item').forEach(c => {
          c.classList.add('visivel');
        });
      } else {
        document.querySelectorAll('.chip-filtro').forEach(c => c.classList.remove('selecionado'));
        chip.classList.add('selecionado');
        quickActive = chip;
        
        document.querySelectorAll('.flashcard-item').forEach(card => {
          const cardVisible = card.dataset.dificuldade === lvl;
          card.classList.toggle('visivel', cardVisible);
        });
      }
      initCarousel();
    });
  });

  // ─── DECK PERSONALIZADO ──────────────────────────────────────────────
  document.querySelectorAll('.chip-disciplinas, .chip-dificuldades').forEach(chip => {
    chip.addEventListener('click', () => {
      chip.classList.toggle('selecionado');
      
      if (quickActive) {
        quickActive.classList.remove('selecionado');
        quickActive = null;
      }
    });
  });

  // Botão "Iniciar Revisão"
  document.getElementById('iniciar-revisao')?.addEventListener('click', () => {
    const selDiscs = Array.from(document.querySelectorAll('.chip-disciplinas.selecionado'))
      .map(c => c.dataset.id);
    const selDiffs = Array.from(document.querySelectorAll('.chip-dificuldades.selecionado'))
      .map(c => c.dataset.id);
    
    document.querySelectorAll('.flashcard-item').forEach(card => {
      const cardDisc = card.dataset.disciplina;
      const cardDiff = card.dataset.dificuldade;
      
      const okDisc = selDiscs.length === 0 || selDiscs.includes(cardDisc);
      const okDiff = selDiffs.length === 0 || selDiffs.includes(cardDiff);
      
      card.classList.toggle('visivel', okDisc && okDiff);
    });

    initCarousel();
  });

  // ─── INICIALIZAÇÃO ──────────────────────────────────────────────────
  document.querySelectorAll('.flashcard-item').forEach(c => c.classList.add('visivel'));
  initCarousel();
});