function initializeApp() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const sidebarClose = document.getElementById('sidebarClose');

    function openSidebar() {
        if (sidebar && sidebarOverlay) {
            sidebar.classList.add('sidebar-moving');
            sidebar.classList.add('active');
            sidebarOverlay.classList.add('active');

            setTimeout(() => {
                sidebar.classList.remove('sidebar-moving');
            }, 600);
        }
    }

    function closeSidebar() {
        if (sidebar && sidebarOverlay) {
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
        }
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', openSidebar);
    }

    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }

    const allLinks = document.querySelectorAll('.nav-link, .sidebar-link');

    allLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            allLinks.forEach(item => item.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {

    const navPlaceholder = document.getElementById('navbar-placeholder');
    const sidebarPlaceholder = document.getElementById('sidebar-placeholder');
    const footerPlaceholder = document.getElementById('footer-placeholder');

    const isInsideComponents =
        window.location.pathname.includes('/components/');

    const basePath = isInsideComponents
        ? '../components/'
        : 'components/';

    const loadNav = fetch(basePath + 'student_navbar.html')
        .then(r => {
            if (!r.ok) throw new Error('Navbar tidak ditemukan');
            return r.text();
        });

    const loadSidebar = fetch(basePath + 'student_sidebar.html')
        .then(r => {
            if (!r.ok) throw new Error('Sidebar tidak ditemukan');
            return r.text();
        });

    const loadFooter = fetch(basePath + 'student_footer.html')
        .then(r => {
            if (!r.ok) throw new Error('Footer tidak ditemukan');
            return r.text();
        });

    Promise.all([loadNav, loadSidebar, loadFooter])
        .then(([navData, sidebarData, footerData]) => {

            if (navPlaceholder) {
                navPlaceholder.innerHTML = navData;
            }

            if (sidebarPlaceholder) {
                sidebarPlaceholder.innerHTML = sidebarData;
            }

            if (footerPlaceholder) {
                footerPlaceholder.innerHTML = footerData;
            }

            initializeApp();
        })
        .catch(err => console.error(err));
});