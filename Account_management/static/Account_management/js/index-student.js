function getBackDates(days){
    let start = sub_days(today, days)
    let start_date = `${start.getFullYear()}-${start.getMonth() + 1}-${start.getDate()}`
    let end_date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
    return {start_date: start_date, end_date: end_date}
}

function getIncomingMeetings() {
    let dates = getFutureDates(30);
    getJson(`/api/meetings-range/?start_date=${dates.start_date}&end_date=${dates.end_date}`)
        .then(data => {
            let mentor = document.querySelector('.student-page .incoming-meetings .student-page-block');
            data.forEach(meeting => {
                let div = createElement('div', mentor, {className: 'meet-box'}),
                    p = createElement('p', div, {className: 'meet-details'}),
                    span = createElement('span', p, {className: 'date'});
                createElement('i', span, {className: 'bi bi-calendar-check',});
                span.append(meeting.date.split("-").reverse().join("."));
                let span2 = createElement('span', p, {className: 'hour', textContent: meeting.hour})
                createElement('i', span2, {className: 'bi bi-clock'})

                let p2 = createElement('p', div),
                    i2 = createElement('i', p2, {className: 'bi bi-person-square'})
                createElement('span', p2, {className: 'student-name', textContent: meeting.person})

            })
            let cal = createElement('div', mentor, {className: 'control-btn'})
            createElement('a', cal, {
                className: 'button', href: "/calendar/",
                textContent: 'show calendar'
            })

        })
}

function getPastMeetings() {
    let dates = getBackDates(30);
    getJson(`/api/meetings-range/?start_date=${dates.start_date}&end_date=${dates.end_date}`)
        .then(data => {
            let mentor = document.querySelector('.student-page .last-meetings .student-page-block');
            data.forEach(meeting => {
                let div = createElement('div', mentor, {className: 'meet-box'}),
                    p = createElement('p', div, {className: 'meet-details'}),
                    span = createElement('span', p, {className: 'date'});
                createElement('i', span, {className: 'bi bi-calendar-check',});
                span.append(meeting.date.split("-").reverse().join("."));
                let span2 = createElement('span', p, {className: 'hour', textContent: meeting.hour})
                createElement('i', span2, {className: 'bi bi-clock'})

                let p2 = createElement('p', div, {className: 'note'})

                showNote(meeting.id, p2)
            })
        })
}

function showNote(id_obj, elment) {
    getJson('/api/notes/?id=' + id_obj)
        .then(data => {
            if (data.length > 0) {
                elment.innerHTML =  data[0].text
            }
        })
}

getIncomingMeetings()
getPastMeetings()