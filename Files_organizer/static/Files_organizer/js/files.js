// carousel splide js:
new Splide('.splide', {
    type: 'loop',
    perMove: 1,
    perPage: 5,
    breakpoints: {
        1450: {
            perPage: 4,
        },
        1200: {
            perPage: 3,
        },
        850: {
            perPage: 2,
        },
        560: {
            perPage: 1,
        }
    }
}).mount();


// pupup on mobile:
const themeName = document.querySelectorAll('a.theme-name.available')
const themeDetails = document.querySelector('.themes-details')
const backBtn = document.querySelector('.back-btn')

const showDetails = () => {
    if (themeDetails.style.display = "none") {
        themeDetails.style.display = "block"
    }
}

const closeDetails = () => {
    if (themeDetails.style.display = "block") {
        themeDetails.style.display = "none"
    }
}

const themeNames = themeName.forEach(name => name.addEventListener('click', showDetails))
backBtn.addEventListener('click', closeDetails)