let today = new Date(),
    currentMonth = today.getMonth(),
    currentYear = today.getFullYear();


function getMeetings() {
    getJson('/api/meetings/?date=' + (currentMonth + 1))
        .then(data => {
            let mentor = document.querySelector('.mentor-page .mentor-page-block');
            data.forEach(meeting => {
                let div = createElement('div', mentor, {className: 'meet-box'}),
                    p = createElement('p', div, {className: 'meet-details'}),
                    span = createElement('span', p, {className: 'date'});
                    createElement('i', span, {className: 'bi bi-calendar-check',});
                    span.append(meeting.date.split("-").reverse().join("."));
                let span2 =  createElement('span', p, {className: 'hour', textContent: meeting.hour})
                createElement('i', span2 ,{className: 'bi bi-clock'})

                let p2 = createElement('p', div),
                    i2 = createElement('i', p2, {className: 'bi bi-person-square'})
                    createElement('span', p2, {className: 'student-name', textContent: meeting.person})

            })
            let cal = createElement('div', mentor, {className: 'control-btn'})
            createElement('a', cal, {className: 'button', href: "http://127.0.0.1:8000/calendar/",
                textContent: 'show calendar'})

        })
}

function getStudents(){
    getJson('/api/students/')
        .then(data => {
            document.querySelector('.your-students span').innerHTML = data.length

        })
}

function getAllMeetings(){
    getJson('/api/all-meetings/')
        .then(data => {
            document.querySelector('.meetings-held-box .meetings-held-count span').innerHTML = data.length

        })
}

async function getJson(url) {
    const response = await fetch(getBaseUrl(url));
    return (await response).json()
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

function createElementBefore(element, elem, args) {
    let d = document.createElement(element);
    if (args) for (const [k, v] of Object.entries(args)) d[k] = v;
    console.log(elem)
    console.log(d)
    elem.append(d);
    return d;
}

getMeetings()
getAllMeetings()
getStudents()