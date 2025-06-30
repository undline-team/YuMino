// Тема
const checkbox = document.getElementById('checkbox');
const body = document.body;

checkbox.addEventListener('change', () => {
    body.classList.toggle('dark-theme');
    localStorage.setItem('theme', body.classList.contains('dark-theme') ? 'dark' : 'light');
});

if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-theme');
    checkbox.checked = true;
}

// Меню бургер
document.addEventListener('DOMContentLoaded', function() {
    const burgerMenuButton = document.querySelector('.burger-menu-button');
    const menu = document.querySelector('.menu');

    if (burgerMenuButton && menu) {
        burgerMenuButton.addEventListener('click', () => {
            menu.classList.toggle('active');
            burgerMenuButton.classList.toggle('active');
        });
    }

    fetch('section_modules.json')
        .then(response => response.json())
        .then(data => {
            const navList = document.getElementById('nav-list');
            const mainContent = document.getElementById('main-content');

            function createSection(sectionData) {
                const section = document.createElement('section');
                section.id = sectionData.id;
                section.classList.add('section', 'hidden');
                section.innerHTML = `<h2>${sectionData.title}</h2>${sectionData.content}`;
                return section;
            }

            function createNavLink(sectionData) {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = '#';
                a.dataset.section = sectionData.id;
                a.textContent = sectionData.title;

                a.addEventListener('click', (e) => {
                    e.preventDefault();
                    const sectionId = sectionData.id;
                    const navLinks = document.querySelectorAll('nav a');
                    const sections = document.querySelectorAll('main section');
                    navLinks.forEach(link => link.classList.remove('active'));
                    sections.forEach(section => section.classList.add('hidden'));

                    if (menu) {
                      menu.classList.remove('active');
                      burgerMenuButton.classList.remove('active');
                    }

                    a.classList.add('active');
                    const sectionElement = document.getElementById(sectionId);
                    if (sectionElement) {
                        sectionElement.classList.remove('hidden');
                    }

                    hljs.highlightAll();
                });

                li.appendChild(a);
                return li;
            }

            data.forEach((sectionData, index) => {
                const section = createSection(sectionData);
                const navLink = createNavLink(sectionData);
                mainContent.appendChild(section);
                navList.appendChild(navLink);
            });

            const firstNavLink = navList.querySelector('a');
            if (firstNavLink) {
                firstNavLink.classList.add('active');
                const firstSectionId = firstNavLink.dataset.section;
                const firstSection = document.getElementById(firstSectionId);
                if (firstSection) {
                    firstSection.classList.remove('hidden');
                }
            }

            hljs.highlightAll();
        })
        .catch(error => console.error('Ошибка загрузки JSON:', error));
});
