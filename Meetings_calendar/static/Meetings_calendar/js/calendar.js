const weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
];



const API_URLS = {
    note: "/api/notes/?id=",
    addNote: "/api/add-note/",
    editNote: "/api/edit-note/",
    meeting: "/api/meeting/?id=",
    allMeetings: "/api/meetings/?year=",
    addMeeting: "/api/add-meeting/",
    editMeeting: "/api/edit-meeting/",
    allStudents: "/api/students/",
}


const CALENDAR_SELECTORS = {
    newEvent: document.querySelector('#addEvent'),
    saveEvent: document.querySelector('#editing-form'),
    addEventModal: document.querySelector('#addEventModal'),
    addEventDate: document.querySelector('#add-event-date'),
    addEventTime: document.querySelector('#add-event-time'),
    editEventBtn: document.querySelector('.edit-event-btn'),
    addEventNote: document.querySelector('#add-event-note'),
    addEventStudent: document.querySelector('#add-event-student'),
    editEventDate: document.querySelector('#edit-event-date'),
    editEventModal2: document.querySelector('#editEventModal2'),
    editEventModalLabel2: document.querySelector('#editEventModalLabel2'),
    editEventNote: document.querySelector('#edit-event-note'),
    editEventNoteLabel: document.querySelector('#edit-event-note_label'),
    editEventTime: document.querySelector('#edit-event-time'),
    editEventStudent: document.querySelector('#edit-event-student'),
    viewNote: document.querySelector('#view-note'),
    noteHour: document.querySelector('.view-time'),
    noteDate: document.querySelector('.view-date'),
    studentName: document.querySelector('.view-student'),
    deleteEventBtn: document.querySelector('.delete-event-btn'),
    deleteNoteBtn: document.querySelector('#delete-note-btn'),
}

CALENDAR_SELECTORS.newEvent.addEventListener('submit', (event) => {
    event.preventDefault();
    newMeeting();
    let modal = bootstrap.Modal.getInstance(CALENDAR_SELECTORS.addEventModal);
    modal.hide()
})

CALENDAR_SELECTORS.saveEvent.addEventListener('submit', (event) => {
    event.preventDefault();
    saveMeeting();
})

CALENDAR_SELECTORS.editEventModal2.addEventListener('hidden.bs.modal',  () => {
    document.getElementById('editing-form').reset();
})

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
                let li = createElement("li", daysBody);
                    createElement("div", li, {className: "date", textContent: date});
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
    getJson(`${API_URLS.allMeetings}${currentYear}&month=${(currentMonth + 1)}`)
        .then(data => {
            viewMeetings(data, args)
        }).catch((error) => {console.log(error)})
}

function viewMeetings(data, args) {
    let where = document.querySelectorAll('#days > li > div');
    let date = 1;
    where.forEach(elem => {
        if (sessionStorage.getItem('isMentor') === 'true') {
            elem.innerHTML = `<span>${date}</span><button type="button" onclick="addEvent(${date})" class="add-event-btn" data-bs-toggle="modal" data-bs-target="#addEventModal"><i class="bi bi-calendar-plus"></i></button>`
        } else {
            elem.innerHTML = `<span>${date}</span>`
        }

        data.forEach(meeting => {
            let meetingDate = meeting.date.split('-'),
                year = parseInt(meetingDate[0]),
                month = parseInt(meetingDate[1]),
                day = parseInt(meetingDate[2]);

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
                eventDesc.innerHTML = `<span class="hour">${meeting.hour}</span>
                <span>${sessionStorage.getItem('isMentor') === 'true' ? meeting.student_name : meeting.mentor_name}</span>`;
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


// function daysInMonth(iMonth, iYear) {
//     return 32 - new Date(iYear, iMonth, 32).getDate();
// }

function showNote(id_obj) {
    getJson(API_URLS.note + id_obj)
        .then(data => {
            if (data.length > 0) {
                CALENDAR_SELECTORS.noteHour.innerHTML = `${data[0].hour}`
                CALENDAR_SELECTORS.noteDate.innerHTML = `${data[0].date} `
                CALENDAR_SELECTORS.editEventBtn.setAttribute('id', id_obj);
                CALENDAR_SELECTORS.editEventBtn.innerHTML = 'Edit';
                if (sessionStorage.getItem('isMentor') === 'true') {
                    CALENDAR_SELECTORS.deleteEventBtn.value = data[0].meeting
                    CALENDAR_SELECTORS.deleteEventBtn.id = data[0].date
                    CALENDAR_SELECTORS.studentName.innerHTML = data[0].student
                } else {
                     CALENDAR_SELECTORS.studentName.innerHTML = data[0].mentor
                }
                if (data[0].text === "") {
                    CALENDAR_SELECTORS.viewNote.textContent = "There is no note for this meeting yet"
                    CALENDAR_SELECTORS.deleteNoteBtn.style.display = 'none'

                } else {
                    CALENDAR_SELECTORS.viewNote.textContent = data[0].text
                    CALENDAR_SELECTORS.deleteNoteBtn.style.display = 'block'
                    CALENDAR_SELECTORS.deleteNoteBtn.value = data[0].date
                }
            }
        }).catch(error => {console.log(error)})
}

function addEvent(date) {
    CALENDAR_SELECTORS.addEventDate.value = new Date(currentYear, currentMonth, date + 1).toISOString().substr(0, 10)
    CALENDAR_SELECTORS.addEventTime.value = ""
    CALENDAR_SELECTORS.addEventNote.value = ""
    let elem = CALENDAR_SELECTORS.addEventStudent;
    setOptionsToNull(elem)
    let option = document.createElement('option');
    option.setAttribute('value', '');
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
        }).catch(error => {console.log(error)})
}

function editNote(id_obj) {
    if (sessionStorage.getItem('isMentor') === 'true') {
        let elem = CALENDAR_SELECTORS.editEventStudent;
        setOptionsToNull(elem);
        getJson(API_URLS.meeting + id_obj)
            .then(data => {
                if (data.length > 0) {
                    CALENDAR_SELECTORS.editEventDate.value = new Date(data[0].date).toISOString().substr(0, 10);
                    CALENDAR_SELECTORS.editEventTime.value = data[0].hour;
                    return data[0].student
                }
            })
            .then(student => {
                getJson(API_URLS.allStudents)
                    .then(data => {
                        if (data.length > 0) {
                            data.forEach(value => {
                                let option = document.createElement('option');
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
                        CALENDAR_SELECTORS.editEventNoteLabel.textContent = 'Note:'
                    })
            })
            .catch(error => {console.log(error)})
    }else {
        CALENDAR_SELECTORS.editEventModalLabel2.textContent = 'Edit note:'
        CALENDAR_SELECTORS.editEventNote.style.marginTop = '15px'
    }
        getJson(API_URLS.note + id_obj)
        .then(data => {
            if (data.length > 0) {
                CALENDAR_SELECTORS.editEventNote.value = data[0].text;
            } else {
                CALENDAR_SELECTORS.editEventNote.value = ""
            }})
            .catch(error => {console.log(error)})
}

function saveMeeting() {
    let meetingId = CALENDAR_SELECTORS.editEventBtn.id;
    if (sessionStorage.getItem('isMentor') === 'true') {
        let date = CALENDAR_SELECTORS.editEventDate.value;
        let hour = CALENDAR_SELECTORS.editEventTime.value;
        let noteTime = `${date} ${hour}`;
        let student = CALENDAR_SELECTORS.editEventStudent;
        let studentId = student.options[student.selectedIndex].id;
        const meeting = {
            'id': meetingId,
            'student': studentId,
            'date': noteTime,
        }
        fetch(getBaseUrl(API_URLS.editMeeting + meetingId + '/'),
            {
                method: "PATCH",
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(meeting),
            })
            // .then(() => saveNote())
            .catch(error => {console.log(error)})
    }
    saveNote()
}

function saveNote() {
    let meeting_data = CALENDAR_SELECTORS.editEventBtn.id;
    let note_text = CALENDAR_SELECTORS.editEventNote.value
    getJson(API_URLS.note + meeting_data)
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
                })
                .catch(error => {console.log(error);})
                .then(() =>{updateCalendarView()})
        })
}

function updateCalendarView(){
    let meeting = document.querySelectorAll('.ev')
    meeting.forEach(element =>{
        element.remove();
    })
    getAllMeetings([currentYear, currentMonth + 1])
}


function newMeeting() {
    let meetingDate = CALENDAR_SELECTORS.addEventDate.value;
    let meetingHour = CALENDAR_SELECTORS.addEventTime.value;
    let meetingTime = `${meetingDate} ${meetingHour}`;
    let student = CALENDAR_SELECTORS.addEventStudent;
    let studentId = student.options[student.selectedIndex].id;
    let mentorId = sessionStorage.getItem('mentorId');
    let note = CALENDAR_SELECTORS.addEventNote.value;
    const meeting = {
        'date': meetingTime,
        'mentor': mentorId,
        'student': studentId,
        'note': note,
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
        })
        .catch(error => {console.log(error);})
        .then(() => {updateCalendarView()})
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
        })
        .catch(error => {console.log(error);})
        .then(() => {updateCalendarView()})
}

function eraseMeeting(meetingId) {
    deleteData(API_URLS.editMeeting + meetingId + '/')
}

function studentOncChange(student_obj) {
    student_obj.options[student_obj.selectedIndex].setAttribute('selected', 'selected');
}

// function set_options_to_null() {
//     Array.from(arguments).forEach(argument => {
//         for (let option = argument.options.length - 1; option >= 0; option--) {
//             argument.options[option] = null;
//         }
//     })
// }
