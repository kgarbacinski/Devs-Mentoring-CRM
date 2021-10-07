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
    console.log('test')
     get_all_meetings([year, month + 1])
}


function get_all_meetings(args) {
    // console.log(get_base_url('/api/meetings/?date=' + (currentMonth + 1)))
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
    console.log(data[0])
    let li = document.querySelectorAll('#days > li > div')
    let date = 1;
    li.forEach(elem => {


        date ++
    })

    // if(sessionStorage.getItem('isMentor') === 'true'){
    //     li.forEach(elem => {
    //         elem.innerHTML = `<span>${date}</span><button type="button" class="add-event-btn" data-bs-toggle="modal" data-bs-target="#addEventModal"><i class="bi bi-calendar-plus"></i></button>`
    //     date ++
    // })
    // }else {
    //     li.forEach(elem => {
    //         elem.innerHTML = `<span>${date}</span>`
    //     date ++
    // })
    // }
    // data.forEach(meeting => {
    //     let date = meeting.date.split('-'),
    //         year = parseInt(date[2]),
    //         month = parseInt(date[1]),
    //         day = parseInt(date[0]);
    //
    // })

    // return (
    //     data &&
    //     data.map((item) => {
    //         // console.log(sessionStorage.getItem('isMentor'))
    //         sessionStorage.setItem('isMentor', item.isMentor);
    //         let date = item.date.split("-"),
    //             year = parseInt(date[2]),
    //             month = parseInt(date[1]) -1,
    //             day = parseInt(date[0]);
                // console.log(year + ' ' + month + ' ' + day)
            // console.log(item)


            // if (year === args[0] && month === args[1] && day === args[2]) {
            //     let event = createElement("div", where, {className: "ev", id: item.id}),
            //         eventDesc = createElement("div", event, {className: "ev-desc"});
            //     // eventDesc.innerHTML = `<span class="hour">${item.content}</span><a href="${item.source}">Student Name</a>
            //     // `;
            //     // MU: zakomentowałam żebyście widzieli jak było oryginalnie - można wykorzystać ${item.source} żeby umieszczać coś, może do notatki, tylko ona nie moze byc widoczna na widoku głównym - dopiero po kliknięciu chyba niech sie zaczytuje do modala edycyjnego?...
            //     eventDesc.innerHTML = `<span class="hour">${item.hour}</span><span>${item.person}</span>
            //     `;
            //     // event.onclick = () => alert(eventDesc.textContent);
            //     event.setAttribute("data-bs-toggle", "modal")
            //     event.setAttribute("data-bs-target", "#editEventModal")
            //     event.setAttribute("type", "button")
            // }
    //     })
    // );
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
// https://dzone.com/articles/determining-number-days-month
function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

// --- Create element
function createElement(element, where, args) {
    let d = document.createElement(element);
    if (args) for (const [k, v] of Object.entries(args)) d[k] = v;
    where.appendChild(d);
    return d;
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

