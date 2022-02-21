let today = new Date(),
    currentMonth = today.getMonth(),
    currentYear = today.getFullYear();

const footerYear = document.querySelector('.year');
const myFileBtn = document.getElementById('myFile');
const fileChosen = document.getElementById('file-chosen');

const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];


myFileBtn.addEventListener('change', function () {
    fileChosen.textContent = this.files[0].name;
})

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

async function getJson(url) {
    const response = await fetch(getBaseUrl(url));
    return (await response).json()
}

function getFutureDates(days) {
    let start = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()} ${today.getHours()}:${today.getMinutes()}`;
    let end = addDays(today, days);
    let end_date = `${end.getFullYear()}-${end.getMonth() + 1}-${end.getDate()} ${end.getHours()}:${end.getMinutes()}`;
    return {start_date: start, end_date: end_date}
}

function getBackDates(days) {
    let start = subDays(today, days)
    let start_date = `${start.getFullYear()}-${start.getMonth() + 1}-${start.getDate()} ${start.getHours()}:${start.getMinutes()}`
    let end_date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()} ${today.getHours()}:${today.getMinutes()}`
    return {start_date: start_date, end_date: end_date}
}

function addDays(date, days) {
    let result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function subDays(date, days) {
    let result = new Date(date);
    result.setDate(result.getDate() - days);
    return result;
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

function showYear() {
    const data = new Date();
    footerYear.textContent = data.getFullYear().toString();
}

function displayAllMeetings() {
    if (sessionStorage.getItem('isMentor') === 'true') {
        let futureDates = getFutureDates(7);
        let querySelector = document.querySelector('.mentor-page .mentor-page-block');
        getMeetings(futureDates, true, querySelector);
    } else {
        let futureDates = getFutureDates(7);
        let pastDates = getBackDates(30);
        let querySelector = document.querySelector('.student-page .incoming-meetings .student-page-block');
        getMeetings(futureDates, false, querySelector);
        querySelector = document.querySelector('.student-page .last-meetings .student-page-block');
        getMeetings(pastDates, false, querySelector, false);
    }
}

function getMeetings(meetingDates, isMentor, querySelector, showCalendarButton = true) {
    let dates = meetingDates
    getJson(`/api/meetings-range/?start_date=${dates.start_date}&end_date=${dates.end_date}`)
        .then(data => {
            data.forEach(meeting => {
                let div = createElement('div', querySelector, {className: 'meet-box'}),
                    p = createElement('p', div, {className: 'meet-details'}),
                    span = createElement('span', p, {className: 'date'});
                createElement('i', span, {className: 'bi bi-calendar-check',});
                span.append(meeting.date.split("-").reverse().join("."));
                let span2 = createElement('span', p, {className: 'hour', textContent: meeting.hour})
                createElement('i', span2, {className: 'bi bi-clock'})

                let p2 = createElement('p', div);
                createElement('i', p2, {className: 'bi bi-person-square'})
                createElement('span', p2, {
                    className: 'student-name',
                    textContent: isMentor ? meeting.student_name : meeting.mentor_name
                })
                if (!showCalendarButton) showNoteText(meeting.id, p2)
            })
            if (showCalendarButton) {
                let calendarButton = createElement('div', querySelector, {className: 'control-btn'})
                createElement('a', calendarButton, {
                    className: 'button', href: "/calendar/",
                    textContent: 'show calendar'
                })
            }
        }).catch((error => {
        console.log(error)
    }))
}

function changeAvatar() {
    let input = document.querySelector('input[type="file"]')
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
        })
        .catch(error => {console.log(error)})
        .then(() => {window.location.reload()})}

function setOptionsToNull() {
    Array.from(arguments).forEach(argument => {
        for (let option = argument.options.length - 1; option >= 0; option--) {
            argument.options[option] = null;
        }
    })
}

function removeAttribute(elem, attr) {
    Array.from(elem.options).forEach(option => {
        option.removeAttribute(attr)
    })
}

function setOptionToSelected(elem, attr){
    Array.from(elem.options).forEach(option => {
        if (option.value === attr){
            option.setAttribute('selected', 'selected')
        }
    })
}

function setAttributes(elem, attrs) {
    for (let key in attrs) {
        elem.setAttribute(key, attrs[key]);
    }
}

function cleanSendData(value = null) {
    if (!value) {
        for (let element in sendData) {sendData[element] = ''}
        return
    }
    sendData[value] = '';
}
function getApiUrl() {
    let url = '?'
    for (let sendDataKey in sendData) {
        if (sendData[sendDataKey]) {
            url += `${sendDataKey}=${sendData[sendDataKey]}&`
        }
    }
    return url
}

