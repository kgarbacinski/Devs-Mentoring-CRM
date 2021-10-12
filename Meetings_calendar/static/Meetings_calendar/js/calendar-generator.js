// demo data for events
// let demo = [
//     {
//         id: "asdfa",
//         date: "2021/10/01",
//         content: "11:00",
//         source: "http://example.com"
//     },
//     {
//         id: "asdfa",
//         date: "2021/10/01",
//         content: "13:30",
//         source: "http://example.com"
//     },
//     {
//         id: "asdfa",
//         date: "2021/10/03",
//         content: "14:30",
//         source: "http://example.com"
//     }
// ];


let today = new Date(),
    currentMonth = today.getMonth(),
    currentYear = today.getFullYear();


// array days of the week
const weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
];
// array of months
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

// structure
let structureCalendar = createElement("div", window.root, {
        id: "structureCalendar"
    }),
    // header
    calendarHeader = createElement("header", structureCalendar, {}),
    // header columns left center and right
    headerLeft = createElement("div", calendarHeader, {className: "left"}),
    headerCenter = createElement("div", calendarHeader, {className: "center"}),
    headerRight = createElement("div", calendarHeader, {className: "right"}),
    // inside left column
    buttonPrev = createElement("button", headerLeft, {innerHTML: `<i class="bi bi-chevron-left"></i>`}),
    buttonNext = createElement("button", headerRight, {innerHTML: `<i class="bi bi-chevron-right"></i>`}),
    centerTitle = createElement("h3", headerCenter, {
        textContent: months[currentMonth] + " " + currentYear
    }),
    // calendar body
    calendarBody = createElement("div", structureCalendar, {id: "calendar"}),
    weekdayBody = createElement("ul", calendarBody, {id: "weekdays"}),
    daysBody = createElement("ul", calendarBody, {id: "days"});

// init calendar
showCalendar(currentMonth, currentYear);

// map week days
weekdays.map((item, i) =>
    // change to monday
    today.getDay() - 1 === i
        ? createElement("li", weekdayBody, {className: "today", textContent: item})
        : createElement("li", weekdayBody, {textContent: item})
);

// buttons next prev
buttonPrev.onclick = () => prev();
buttonNext.onclick = () => next();

// generate calendar
function showCalendar(month, year) {
    // first day - 1
    let firstDay = new Date(year, month).getDay() - 1;

    // clear preview content
    daysBody.textContent = "";

    // filing data about month and in the page via DOM.
    centerTitle.textContent = months[month] + " " + year;

    // creating all cells
    let date = 1;
    for (let i = 0; i < 6; i++) {
        //creating individual cells, filing them up with data.
        for (let j = 0; j < 7; j++) {
            if (i === 0 && j < firstDay) {
                createElement("li", daysBody, {textContent: ""});
            } else if (date > daysInMonth(month, year)) {
                break;
            } else {
                let li = createElement("li", daysBody, {}),
                    div = createElement("div", li, {className: "date", textContent: date});
                if (
                    date === today.getDate() &&
                    year === today.getFullYear() &&
                    month === today.getMonth()
                ) {
                    li.className = "today";
                }
                date++;
            }
        }
    }
    get_all_meetings([year, month + 1])
}


function get_all_meetings(args) {
    console.log(get_base_url('/api/meetings/?date=' + (currentMonth + 1)))
    fetch(get_base_url('/api/meetings/?date=' + (currentMonth + 1)))
        .then(resp => {
            return resp.json()
        })
        .then(data => {
            viewEvents(data, args)
        })
}

function get_base_url(path) {
    let protocol = window.location.protocol;
    let host = window.location.host;
    return `${protocol}//${host ? host : ""}${path}`
}

// view events
function viewEvents(data, args) {
    // console.log(data[0])
    let where = document.querySelectorAll('#days > li > div')
    let date = 1;
    where.forEach(elem => {
        if (sessionStorage.getItem('isMentor') === 'true') {
            elem.innerHTML = `<span>${date}</span><button type="button" class="add-event-btn" data-bs-toggle="modal" data-bs-target="#addEventModal"><i class="bi bi-calendar-plus"></i></button>`
        } else {
            elem.innerHTML = `<span>${date}</span>`
        }

        data.forEach(meeting => {
            let whole_ddate = meeting.date.split('-'),
                year = parseInt(whole_ddate[0]),
                month = parseInt(whole_ddate[1]),
                day = parseInt(whole_ddate[2]);

            if (year === args[0] && month === args[1] && day === date) {
                let event = createElement("button", elem.parentElement, {
                    className: "ev",
                    id: `${meeting.id};${meeting.date};${meeting.hour}`
                });
                event.setAttribute("data-bs-toggle", "modal")
                event.setAttribute("data-bs-target", "#editEventModal")
                event.setAttribute("type", "button")
                event.setAttribute('onclick', 'showNote(this.id)')
                let eventDesc = createElement("div", event, {className: "ev-desc"});
                eventDesc.innerHTML = `<span class="hour">${meeting.hour}</span><span>${meeting.person}</span>`;

            }
        })
        date++
    })
}

// next month
function next() {
    currentMonth = (currentMonth + 1) % 12;
    currentYear = currentMonth === 0 ? currentYear + 1 : currentYear;
    showCalendar(currentMonth, currentYear);
}

// previus month
function prev() {
    currentMonth = currentMonth === 0 ? 11 : currentMonth - 1;
    currentYear = currentMonth === 11 ? currentYear - 1 : currentYear;
    showCalendar(currentMonth, currentYear);
}

// check how many days in a month code from
function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

// --- Create element
function createElement(element, elem, args) {
    let d = document.createElement(element);
    if (args) for (const [k, v] of Object.entries(args)) d[k] = v;
    elem.appendChild(d);
    return d;
}

//TODO finish function for creating meeting in proper order
function createMeeting() {

}

// MU: functions for editing modal
const editEventBtn = document.querySelector('.edit-event-btn')
const previewEvent = document.querySelector('.preview-event')
const editingForm = document.querySelector('.editing-form')
const cancelEventBtn = document.querySelector('.edit-cancel-event-btn')

const showEditForm = () => {
    editingForm.style.display = 'unset'
    previewEvent.style.display = 'none'
}

const closeForm = () => {
    previewEvent.style.display = 'unset'
    editingForm.style.display = 'none'
}


editEventBtn.addEventListener('click', showEditForm)
cancelEventBtn.addEventListener('click', closeForm)

//RG functions


function showNote(id_obj) {
    // console.log(id_obj)
    let view_note = document.querySelector('#view-note');
    let note_hour = document.querySelector('#note-hour');
    fetch(get_base_url('/api/notes/?id=' + id_obj.split(';')[0]))
        .then(resp => {
            return resp.json()
        })
        .then(data => {
            document.querySelector('.edit-event-btn').setAttribute('id', id_obj)
            if (data.length > 0) {
                note_hour.innerHTML = data[0].hour
                view_note.innerHTML = data[0].text

            } else {
                note_hour.innerHTML = ""
                view_note.innerHTML = ""
            }
        })
}

function editNote(id_obj) {
    console.log(id_obj)
    document.querySelector('#edit-note').innerHTML = document.querySelector('#view-note').innerHTML;
    document.querySelector('#edit-event-time').value = id_obj.split(';')[2];
    document.querySelector('#edit-event-date').value = new Date(id_obj.split(';')[1]).toISOString().substr(0, 10)
    fetch(get_base_url('/api/students/'))
        .then(resp => {
            return resp.json()
        })
        .then(data => {
            // console.log(data)
            if (data.length > 0) {
                data.forEach(value => {
                    let elem = document.querySelector('#edit-event-student')
                    let option = document.createElement('option');
                    // option.setAttribute('selected', 'selected')
                    option.innerHTML = value.student;
                    elem.appendChild(option)
                })

            }
        })
}

function saveNote() {
    let meeting_data = document.querySelector('.edit-event-btn').id
    let hour = document.querySelector('#edit-event-time').value;
    let date = document.querySelector('#edit-event-date').value;
    let note = document.querySelector('#edit-note').value;
    // console.log(date)
    let dupa = new Date('2021-10-07:15:30')
    console.log(dupa)
    let url = get_base_url('/api/meeting-edit/' + meeting_data.split(';')[0])
    fetch(url, {

        // Adding method type
        method: "POST",

        // Adding body or contents to send
        body: JSON.stringify({
            id: 4,
            date: dupa,
            mentor: 1,
            student: 1,
        }),

        // Adding headers to the request
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
        .then(response => response.json())
        .then(json => console.log(json));
}

// function newMeeting(){
//     let date_new = new Date()
//     let mentor_a = 4
//     let student_a = 3
//
//     const url = 'http://127.0.0.1:8000/api/meeting-add/';
//
//     const meeting = {
//     date: date_new,
//     mentor: mentor_a,
//     student: student_a
// };
//
// // request options
// const options = {
//     method: 'POST',
//     body: JSON.stringify(meeting),
//     headers: {
//         'Content-Type': 'application/json'
//     }
// }
//
// // send POST request
// fetch(url, options)
//     .then(res => res.json())
//     .then(res => console.log(res));
// }

function newMeeting() {
    let formData = new FormData();


    let date_new = new Date()
    date_new.toLocaleString()
    let mentor_a = 4
    let student_a = 3
    formData.append('date', '12.10.2021 10:00');
    formData.append('mentor', '4');
    formData.append('student', '3');

    fetch("http://127.0.0.1:8000/api/meeting-add/",
        {
            method: "post",
            mode : 'same-origin',
            credentials: 'same-origin',
            contentType: 'application/json',
            body: formData,
        }).catch((error => {
            console.log(error);
    }));
}