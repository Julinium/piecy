
// JavaScript to handle the navbar shrinking effect
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const classes_shrunk = ['shadow', 'bg-warning-subtle', 'py-0', 'my-0']
    const classes_expand = ['pt-3', 'mb-5']

    if (window.scrollY > 0) { // Adjust scroll threshold as needed
        for (cs in classes_shrunk) {
            navbar.classList.add(classes_shrunk[cs]);
        }
        for (ce in classes_expand) {
            navbar.classList.remove(classes_expand[ce]);
        }

    } else {
        for (cs in classes_shrunk) {
            navbar.classList.remove(classes_shrunk[cs]);
        }
        for (ce in classes_expand) {
            navbar.classList.remove(classes_expand[ce]);
        }
    }
});
