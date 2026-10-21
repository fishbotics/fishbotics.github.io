const backgroundLinks = document.querySelectorAll('.secret[data-background]');

backgroundLinks.forEach(link => {
    link.addEventListener('click', () => {
        document.body.style.backgroundImage = `url("${link.dataset.background}")`;
        backgroundLinks.forEach(candidate => {
            candidate.classList.toggle('is-active', candidate === link);
        });
    });
});
