document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidade para dispositivos móveis
    const menuToggle = document.createElement('div');
    menuToggle.classList.add('menu-toggle');
    menuToggle.innerHTML = '<span class="material-symbols-outlined">menu</span>';
    document.body.appendChild(menuToggle);
    
    menuToggle.addEventListener('click', function() {
        document.querySelector('.sidebar').classList.toggle('active');
        document.querySelector('.content').classList.toggle('pushed');
    });
    
    // Fechar menu ao clicar em um item (apenas mobile)
    if (window.innerWidth <= 768) {
        const menuItems = document.querySelectorAll('.menu-content li a');
        menuItems.forEach(item => {
            item.addEventListener('click', function() {
                document.querySelector('.sidebar').classList.remove('active');
                document.querySelector('.content').classList.remove('pushed');
            });
        });
    }
});