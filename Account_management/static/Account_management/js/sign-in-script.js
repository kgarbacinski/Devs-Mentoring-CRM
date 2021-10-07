const resetLink = document.querySelector('.reset-link')
const popup = document.querySelector('.popup')
const resetBtn = document.querySelector('.reset')
// const resetBtn = document.querySelector('.reset')
const cancelBtn = document.querySelector('.cancel')

//
const showPopup = () => {
    popup.style.display = "flex"
}

const closePopup = () => {
    popup.style.display = "none"
}

//
resetLink.addEventListener('click', showPopup)
cancelBtn.addEventListener('click', closePopup)

signInBtn.addEventListener('click', e => {
    e.preventDefault();
})
resetBtn.addEventListener('click', e => {
    e.preventDefault();
})
cancelBtn.addEventListener('click', e => {
    e.preventDefault();
})
//
// signInBtn.addEventListener('click', e => {
//     e.preventDefault();
// })
// resetBtn.addEventListener('click', e => {
//     e.preventDefault();
// })
// cancelBtn.addEventListener('click', e => {
//     e.preventDefault();
// })
