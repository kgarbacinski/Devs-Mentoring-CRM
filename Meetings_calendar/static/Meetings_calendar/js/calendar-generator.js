const weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
];

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

const API_URLS = {
    note: "/api/notes/?id=",
    addNote: "/api/add-note/",
    editNote: "/api/edit-note/",
    meeting: "/api/meeting/?id=",
    allMeetings: "/api/meetings/?date=",
    addMeeting: "/api/add-meeting/",
    editMeeting: "/api/edit-meeting/",
    allStudents: "/api/students/",
}


let structureCalendar = createElement("div", window.root, {
        id: "structureCalendar"
    }),
    calendarHeader = createElement("header", structureCalendar, {}),
    headerLeft = createElement("div", calendarHeader, {className: "left"}),
    headerCenter = createElement("div", calendarHeader, {className: "center"}),
    headerRight = createElement("div", calendarHeader, {className: "right"}),
    buttonPrev = createElement("button", headerLeft, {innerHTML: `<i class="bi bi-chevron-left"></i>`}),
    buttonNext = createElement("button", headerRight, {innerHTML: `<i class="bi bi-chevron-right"></i>`}),
    centerTitle = createElement("h3", headerCenter, {
        textContent: months[currentMonth] + " " + currentYear
    }),
    calendarBody = createElement("div", structureCalendar, {id: "calendar"}),
    weekdayBody = createElement("ul", calendarBody, {id: "weekdays"}),
    daysBody = createElement("ul", calendarBody, {id: "days"});
calendarHeader.setAttribute('style', 'z-index: 97');
showCalendar(currentMonth, currentYear);

weekdays.map((item, i) =>
    today.getDay() - 1 === i
        ? createElement("li", weekdayBody, {className: "today", textContent: item})
        : createElement("li", weekdayBody, {textContent: item})
);

buttonPrev.onclick = () => prev();
buttonNext.onclick = () => next();

function showCalendar(month, year) {
    let firstDay = new Date(year, month).getDay() - 1;
    daysBody.textContent = "";
    centerTitle.textContent = months[month] + " " + year;
    let date = 1;
    for (let i = 0; i < 6; i++) {
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
    getAllMeetings([year, month + 1])
}


function getAllMeetings(args) {
    getJson(API_URLS.allMeetings + (currentMonth + 1))
        .then(data => {
            viewMeetings(data, args)
        })
}

function setAttributes(elem, attrs) {
    for (let key in attrs) {
        elem.setAttribute(key, attrs[key]);
    }
}

function viewMeetings(data, args) {
    let where = document.querySelectorAll('#days > li > div');
    // let student_name = document.querySelector('.view-student');
    let date = 1;
    where.forEach(elem => {
        if (sessionStorage.getItem('isMentor') === 'true') {
            elem.innerHTML = `<span>${date}</span><button type="button" onclick="addEvent(${date})" class="add-event-btn" data-bs-toggle="modal" data-bs-target="#addEventModal"><i class="bi bi-calendar-plus"></i></button>`
        } else {
            elem.innerHTML = `<span>${date}</span>`
        }

        data.forEach(meeting => {
            let meeting_date = meeting.date.split('-'),
                year = parseInt(meeting_date[0]),
                month = parseInt(meeting_date[1]),
                day = parseInt(meeting_date[2]);

            if (year === args[0] && month === args[1] && day === date) {
                let event = createElement("button", elem.parentElement, {
                    className: "ev",
                    id: `${meeting.id}`
                });
                setAttributes(event, {
                    "data-bs-toggle": "modal",
                    "data-bs-target": "#editEventModal",
                    "type": "button",
                    "onclick": "showNote(this.id)"
                })
                let eventDesc = createElement("div", event, {className: "ev-desc"});
                if (sessionStorage.getItem('isMentor') === 'true') {
                    eventDesc.innerHTML = `<span class="hour">${meeting.hour}</span><span>${meeting.student_name}</span>`;
                } else {
                    eventDesc.innerHTML = `<span class="hour">${meeting.hour}</span><span>${meeting.mentor_name}</span>`;
                }


            }
        })
        date++
    })
}

function next() {
    currentMonth = (currentMonth + 1) % 12;
    currentYear = currentMonth === 0 ? currentYear + 1 : currentYear;
    showCalendar(currentMonth, currentYear);

}

function prev() {
    currentMonth = currentMonth === 0 ? 11 : currentMonth - 1;
    currentYear = currentMonth === 11 ? currentYear - 1 : currentYear;
    showCalendar(currentMonth, currentYear);
}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}


async function getNote(url, meeting_id) {
    const response = await (getJson(url + meeting_id));
    // console.log(await response)
    return (await response)
}

function test() {
    getNote(API_URLS.note, 100)
        .then(data => {
            console.log(data)
        })
}

test()

function showNote(id_obj) {
    let view_note = document.querySelector('#view-note');
    let note_hour = document.querySelector('#note-hour');
    let student_name = document.querySelector('.view-student');
    getJson(API_URLS.note + id_obj)
        .then(data => {
            if (data.length > 0) {
                console.log(data);
                note_hour.innerHTML = `${data[0].date}   ${data[0].hour}`
                document.querySelector('.edit-event-btn').setAttribute('id', id_obj)
                document.querySelector('.edit-event-btn').innerHTML = 'Edit'
                if (sessionStorage.getItem('isMentor') === 'true') {
                    document.querySelector('.delete-event-btn').value = data[0].id
                    student_name.innerHTML = data[0].student
                } else {
                    student_name.innerHTML = data[0].mentor
                }
                if (data[0].text === '') {
                    view_note.value = "There is no note for this meeting yet"
                } else {
                    view_note.value = data[0].text
                }
            }
        })
}

function addEvent(date) {
    document.querySelector('#add-event-date').value = new Date(currentYear, currentMonth, date + 1).toISOString().substr(0, 10)
    let elem = document.querySelector('#add-event-student');
    set_options_to_null(elem)
    let option = document.createElement('option');
    option.setAttribute('value', '');
    // option.setAttribute('disabled', 'disabled');
    option.innerHTML = '-- choose --';
    elem.appendChild(option)

    getJson(API_URLS.allStudents)
        .then(data => {
            if (data.length > 0) {
                data.forEach(value => {
                    let option = document.createElement('option');
                    option.innerHTML = value.student;
                    option.id = value.id
                    elem.appendChild(option)
                })
            }
        })

}

function editNote(id_obj) {
    if (sessionStorage.getItem('isMentor') === 'true') {
        // document.querySelector('.modal-footer').style.display = 'unset'
        // document.querySelector('#delete-event-txt').innerHTML = 'Delete meeting'
        let elem = document.querySelector('#edit-event-student');
        set_options_to_null(elem);
        getJson(API_URLS.meeting + id_obj)
            .then(data => {
                if (data.length > 0) {
                    document.querySelector('#edit-event-date').value = new Date(data[0].date).toISOString().substr(0, 10)
                    document.querySelector('#edit-event-time').value = data[0].hour
                    return data[0].student
                }
            })
            .then(student => {
                getJson(API_URLS.allStudents)
                    .then(data => {
                        if (data.length > 0) {

                            data.forEach(value => {
                                // let elem = document.querySelector('#edit-event-student')
                                let option = document.createElement('option');
                                // option.setAttribute('selected', 'selected')
                                option.innerHTML = value.student;
                                option.id = value.id
                                elem.appendChild(option)
                            })
                            Array.from(elem.options).forEach(option => {
                                if (parseInt(option.id) === student) {
                                    option.setAttribute('selected', 'selected')
                                }
                            })

                        }
                    }).then(() => {
                    getJson(API_URLS.note + id_obj)
                        .then(data => {
                            if (data.length > 0) {
                                document.querySelector('#edit-event-note').value = data[0].text
                            } else {
                                document.querySelector('#edit-event-note').value = ""
                            }
                        }).catch((error => {
                        console.log(error)
                    }))
                })
            })
    }
}

function saveMeeting() {
    let meeting_data = document.querySelector('.edit-event-btn').id;
    if (sessionStorage.getItem('isMentor') === 'true') {
        let hour = document.querySelector('#edit-event-time').value;
        let date = document.querySelector('#edit-event-date').value;
        let note_time = `${date} ${hour}`;
        let student = document.querySelector('#edit-event-student');
        let student_id = student.options[student.selectedIndex].id;
        const meeting = {
            'id': meeting_data,
            'student': student_id,
            'date': note_time,
        }
        fetch(getBaseUrl(API_URLS.editMeeting + meeting_data + '/'),
            {
                method: "PATCH",
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(meeting),
            }).catch((error => {
            console.log(error)
        }))
    }
    saveNote()
}

function saveNote(del='false') {
    let meeting_data = document.querySelector('.edit-event-btn').id;
    let note_text = ''
    if(del === 'true'){
        note_text = '';
    }else {
        note_text = document.querySelector('#edit-event-note').value;
    }

    const note = {
        'text': note_text,
        'meeting': meeting_data,
        'author': sessionStorage.getItem('userId')
    };
    getNote(API_URLS.note, meeting_data)
        .then(data => {
            return data[0].id
        })
        .then(note_id => {
            const editNote = {
                'id': note_id,
                'text': note_text
            };
            fetch(getBaseUrl(API_URLS.editNote + note_id + '/'),
                {
                    method: "PATCH",
                    credentials: 'same-origin',
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(editNote)
                }).catch((error => {
                console.log(error);
            }));
        })
}


let form = document.querySelector('#addEvent');
form.addEventListener('submit', (event) => {
    event.preventDefault();
    newMeeting();
})

function newMeeting() {
    let meeting_date = document.querySelector('#add-event-date').value;
    let meeting_hour = document.querySelector('#add-event-time').value;
    let meeting_time = `${meeting_date} ${meeting_hour}`;
    let student = document.querySelector('#add-event-student');
    let student_id = student.options[student.selectedIndex].id;
    let mentor_id = sessionStorage.getItem('mentorId');
    let note = document.querySelector('#add-event-note').value;
    console.log(note)
    const meeting = {
        'date': meeting_time,
        'mentor': mentor_id,
        'student': student_id,
        'note': note
    };

    fetch(getBaseUrl(API_URLS.addMeeting),
        {
            method: "post",
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                "Content-Type": "application/json"

            },
            body: JSON.stringify(meeting),
        }).catch((error => {
        console.log(error);
    }));
    window.location.reload();
}

function deleteData(url) {
    fetch(getBaseUrl(url),
        {
            method: "DELETE",
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: null,
        }).catch((error => {
        console.log(error);
    }));
}

function eraseMeeting(mentor_note_id) {
    let meeting_id = document.querySelector('.edit-event-btn').id;
    deleteData(API_URLS.editMeeting + meeting_id + '/')
    window.location.reload();
}


function deleteEvent(note_id) {
    if (document.querySelector('#delete-note-txt').textContent === 'Delete note:' && note_id) {
        deleteData(API_URLS.editNote + note_id + '/')
    } else {
        let meeting_data = document.querySelector('.edit-event-btn').id;
        deleteData(API_URLS.editMeeting + meeting_data + '/')
    }
    window.location.reload();
}


function studentOncChange(student_obj) {
    student_obj.options[student_obj.selectedIndex].setAttribute('selected', 'selected');
}

function set_options_to_null() {
    Array.from(arguments).forEach(argument => {
        for (let option = argument.options.length - 1; option >= 0; option--) {
            argument.options[option] = null;
        }
    })
}
