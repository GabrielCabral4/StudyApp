document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.createElement('div');
    menuToggle.classList.add('menu-toggle');
    menuToggle.innerHTML = '<span class="material-symbols-outlined">menu</span>';
    document.body.appendChild(menuToggle);
    
    menuToggle.addEventListener('click', function() {
        document.querySelector('.sidebar').classList.toggle('active');
        document.querySelector('.content').classList.toggle('pushed');
    });
    
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

document.addEventListener('DOMContentLoaded', () => {
    const filtroForm = document.getElementById('form-filtros-anotacoes');
    const selects = filtroForm.querySelectorAll('select');
    const spinner = document.getElementById('loading-spinner');

    selects.forEach(select => {
        select.addEventListener('change', () => {
            spinner.style.display = 'flex'; // mostra o spinner
            filtroForm.submit();
        });
    });
});
