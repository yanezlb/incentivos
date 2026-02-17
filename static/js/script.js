const hamBurger = document.querySelector(".toggle-btn");
const sidebar = document.getElementById('sidebar');
const usuarioMenu = document.querySelector("#m-usuario");
const iconPreview3 = document.querySelector('.icon-preview3');
let openSubmenu = null;

// Initialize sidebar state
document.addEventListener("DOMContentLoaded", () => {
    iconPreview3.style.display = 'none';
    initSubmenuBehavior();
});

function initSubmenuBehavior() {
    // Close all submenus when clicking outside
    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && openSubmenu) {
            closeAllSubmenus();
        }
    });

    // Handle sidebar clicks
    sidebar.addEventListener('click', (e) => {
        const toggle = e.target.closest('[data-bs-toggle="collapse"]');
        
        if (toggle && !sidebar.classList.contains('expand')) {
            handleCollapsedMenuClick(toggle, e);
        }
    });
}

function handleCollapsedMenuClick(toggle, e) {
    e.preventDefault();
    const target = document.querySelector(toggle.getAttribute('href'));
    
    if (openSubmenu && openSubmenu !== target) {
        closeAllSubmenus();
    }
    
    target.classList.toggle('show');
    openSubmenu = target.classList.contains('show') ? target : null;
    
    // Adjust scroll position
    const parentItem = toggle.closest('.sidebar-item');
    const sidebarNav = document.querySelector('.sidebar-nav');
    const scrollPosition = parentItem.offsetTop - sidebarNav.offsetTop;
    
    sidebarNav.scrollTo({
        top: scrollPosition,
        behavior: 'smooth'
    });
}

function closeAllSubmenus() {
    document.querySelectorAll('.sidebar-dropdown').forEach(sub => {
        sub.classList.remove('show');
    });
    openSubmenu = null;
}

// Toggle sidebar
hamBurger.addEventListener("click", function () {
    sidebar.classList.toggle("expand");
    closeAllSubmenus();
    
    if (sidebar.classList.contains("expand")) {
        usuarioMenu.classList.remove("d-none");
        iconPreview3.style.display = 'none';
    } else {
        usuarioMenu.classList.add("d-none");
        iconPreview3.style.display = 'inline';
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sidebar.classList.remove("expand");
        usuarioMenu.classList.add("d-none");
        iconPreview3.style.display = 'block';
        closeAllSubmenus();
    } else {
        usuarioMenu.classList.remove("d-none");
        iconPreview3.style.display = 'none';
    }
});
