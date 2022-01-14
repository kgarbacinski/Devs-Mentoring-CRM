function getMeetings() {
    let dates = getFutureDates(7);
    getJson(`/api/meetings-range/?start_date=${dates.start_date}&end_date=${dates.end_date}`)
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
                    createElement('span', p2, {className: 'student-name', textContent: meeting.student_name})

            })
            let cal = createElement('div', mentor, {className: 'control-btn'})
            createElement('a', cal, {className: 'button', href: "/calendar/",
                textContent: 'show calendar'})

        })
}

getMeetings()
