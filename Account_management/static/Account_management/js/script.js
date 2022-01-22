let today = new Date(),
    currentMonth = today.getMonth(),
    currentYear = today.getFullYear();

async function getJson(url) {
    const response = await fetch(getBaseUrl(url));
    return (await response).json()
}

function getFutureDates(days){
    let start = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
    let end = add_days(today, days);
    let end_date = `${end.getFullYear()}-${end.getMonth() + 1}-${end.getDate()}`
    return {start_date: start, end_date: end_date}
}


function getBaseUrl(path) {
    let protocol = window.location.protocol;
    let host = window.location.host;
    return `${protocol}//${host ? host : ""}${path}`
}

function createElement(element, elem, args) {
    let d = document.createElement(element);
    if (args) for (const [k, v] of Object.entries(args)) d[k] = v;
    elem.appendChild(d);
    return d;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function add_days(date, days) {
    let result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function sub_days(date, days) {
    let result = new Date(date);
    result.setDate(result.getDate() - days);
    return result;
}


const footerYear = document.querySelector('.year')

function showYear() {
    const data = new Date();
    footerYear.textContent = data.getFullYear().toString();
}
showYear()

const myFileBtn = document.getElementById('myFile');
const fileChosen = document.getElementById('file-chosen');

myFileBtn.addEventListener('change', function(){
  fileChosen.textContent = this.files[0].name;

})

function changeAvatar(){
    let input = document.querySelector('input[type="file"]')
task-list
    let userId = sessionStorage.getItem('mentorId')
    let data = new FormData()
    data.append('id', userId)
    data.append('user_image', input.files[0])

    fetch(getBaseUrl('/api/change-avatar/' + userId + '/'),
            {
                method: "PATCH",
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: data,
            }).catch((error => {
                console.log(error)
        })).then(() => {window.location.reload()})
}
