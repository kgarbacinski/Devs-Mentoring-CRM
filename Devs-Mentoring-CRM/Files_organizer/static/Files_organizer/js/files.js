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
