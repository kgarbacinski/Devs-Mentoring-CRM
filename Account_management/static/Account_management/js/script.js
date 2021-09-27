const footerYear = document.querySelector('.year')

function showYear() {
    const data = new Date();

    let year = data.getYear();
    if (year < 1000) {
        year = 2000 + year - 100;
    }
    footerYear.textContent = year
}
showYear()