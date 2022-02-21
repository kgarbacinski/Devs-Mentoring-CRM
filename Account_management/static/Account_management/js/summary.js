let sendData = {
    year: '',
    month: '',
    day: '',
    mentor: '',
    student: '',
    path: ''
}

const SELECTORS =  {
    yearsList: document.getElementById('years'),
    monthsList: document.getElementById('months'),
    daysList: document.getElementById('days'),
    studentsList: document.getElementById('students'),
    pathsList: document.getElementById('paths'),
    tableElement: document.getElementById("listing"),
    btnDisplayAll: document.getElementById('display_all')
};
const API = {
    table: '/api/all-meetings/',
    allPaths: '/api/all-paths/',
    allStudents: '/api/all-students/',
    allYears: '/api/meeting-dates/',
    allMonths: '/api/meeting-dates/?year=',
    meetingDates: '/api/meeting-dates/'
};

if (IS_MODERATOR) {
    SELECTORS.mentorsList = document.getElementById('mentors');
    API.allMentors = '/api/all-mentors/';
}


document.addEventListener('DOMContentLoaded', function () {
    getYears()
}, false);


SELECTORS.btnDisplayAll.addEventListener('click', function () {
    cleanSendData();
    getYears();
})

SELECTORS.yearsList.addEventListener('change', function () {
    removeAttribute(SELECTORS.yearsList, 'selected');
    cleanSendData();
    this.options[this.selectedIndex].setAttribute('selected', 'selected');
    if (this.value !== 'all') sendData.year = this.value;
    getMonths();
});

SELECTORS.monthsList.addEventListener('change', function () {
    removeAttribute(SELECTORS.monthsList, 'selected');
    cleanSendData('month');
    this.options[this.selectedIndex].setAttribute('selected', 'selected');
    if (this.value !== 'all') sendData.month = this.value;
    getDays();
});

SELECTORS.daysList.addEventListener('change', function () {
    removeAttribute(SELECTORS.daysList, 'selected');
    cleanSendData('day');
    this.options[this.selectedIndex].setAttribute('selected', 'selected');
    if (this.value !== 'all') sendData.day = this.value;
    if (IS_MODERATOR) {
        getMentors();
    } else {
        getStudents()
    }

});
if (IS_MODERATOR) {
    SELECTORS.mentorsList.addEventListener('change', function () {
        removeAttribute(SELECTORS.mentorsList, 'selected');
        cleanSendData('mentor');
        this.options[this.selectedIndex].setAttribute('selected', 'selected');
        if (this.value !== 'all') {
            sendData.mentor = this.value;
            getStudents();
        } else {
            getMentors();
        }

    });
}

SELECTORS.studentsList.addEventListener('change', function () {
    removeAttribute(SELECTORS.studentsList, 'selected');
    cleanSendData('student');
    this.options[this.selectedIndex].setAttribute('selected', 'selected');
    if (this.value !== 'all') {
        sendData.student = this.value;
        if (IS_MODERATOR) {
            getMentors();
        } else {
            getPaths();
        }
    } else {
        getStudents();
    }
});

SELECTORS.pathsList.addEventListener('change', function () {
    removeAttribute(SELECTORS.pathsList, 'selected');
    cleanSendData('path');
    this.options[this.selectedIndex].setAttribute('selected', 'selected');
    if (this.value !== 'all') sendData.path = this.value;
    putTable();
});

function getYears() {
    SELECTORS.yearsList.textContent = '';
    getJson(API.meetingDates)
        .then(data => {
            createElement('option', SELECTORS.yearsList,
                {'value': 'all', 'text': 'All Years'});
            data.forEach(option => {
                createElement('option', SELECTORS.yearsList,
                    {'value': option.year, 'text': option.year});
                if (option.year === currentYear) {
                    sendData.year = currentYear;
                    setOptionToSelected(SELECTORS.yearsList, currentYear.toString());
                }
            })
        })
        .then(() => {
            if (!sendData.year) setOptionToSelected(SELECTORS.yearsList, 'all');
            getMonths();
        })
}

function getMonths() {
    cleanSendData('month');
    SELECTORS.monthsList.textContent = '';
    if (!sendData.year) {
        for (let i = 0; i < months.length; i++) {
            createElement('option', SELECTORS.monthsList,
                {value: i, text: months[i]});
        }
        getDays()
        return
    }
    getJson(API.meetingDates + getApiUrl())
        .then(data => {
            createElement('option', SELECTORS.monthsList,
                {'value': 'all', 'text': 'All Months'});
            data.forEach(option => {
                createElement('option', SELECTORS.monthsList,
                    {value: option.month, text: months[option.month - 1]});
                if ((option.year === currentYear) && (option.month = currentMonth + 1)) {
                    sendData.month = currentMonth + 1;
                    setOptionToSelected(SELECTORS.monthsList, (currentMonth + 1).toString());
                } else {
                    sendData.month = SELECTORS.monthsList.options[1].value;
                    SELECTORS.monthsList.options[1].setAttribute('selected', 'selected');
                }
            })
        })
        .then(() => {
            getDays();
        })
}

function getDays() {
    SELECTORS.daysList.textContent = '';
    if (!sendData.month) {
        createElement('option', SELECTORS.daysList,
            {'value': 'all', 'text': 'All Days'});
        for (let i = 1; i <= 31; i++) {
            createElement('option', SELECTORS.daysList,
                {'value': i, 'text': i});
        }
        if (IS_MODERATOR) {
            getMentors()
        } else {
            getStudents()
        }
        return
    }
    getJson(API.meetingDates + getApiUrl())
        .then(data => {
            createElement('option', SELECTORS.daysList,
                {'value': 'all', 'text': 'All Days'});
            data.forEach(option => {
                createElement('option', SELECTORS.daysList,
                    {value: option.day, text: option.day});
            })
        })
        .then(() => {
            setOptionToSelected(SELECTORS.daysList, sendData.day.toString());
            if (IS_MODERATOR) {
                getMentors()
            } else {
                getStudents()
            }
        })
}

function getMentors() {
    SELECTORS.mentorsList.textContent = ''
    getJson(API.allMentors + getApiUrl())
        .then(data => {
            createElement('option', SELECTORS.mentorsList,
                {'value': 'all', 'text': 'All Mentors'});
            data.forEach(option => {
                createElement('option', SELECTORS.mentorsList,
                    {'value': option.id, 'text': option.name});
            })
        })
        .then(() => {
            setOptionToSelected(SELECTORS.mentorsList, sendData.mentor.toString());
            if (!sendData.student) {
                getStudents();
            } else {
                getPaths();
            }
        })

}

function getStudents() {
    SELECTORS.studentsList.textContent = '';
    getJson(API.allStudents + getApiUrl())
        .then(data => {
            createElement('option', SELECTORS.studentsList,
                {'value': 'all', 'text': 'All Students'});
            data.forEach(option => {
                createElement('option', SELECTORS.studentsList,
                    {'value': option.id, 'text': option.name});
            })
        })
        .then(() => {
            setOptionToSelected(SELECTORS.studentsList, sendData.student.toString());
            getPaths();
        })
}

function getPaths() {
    SELECTORS.pathsList.textContent = '';
    getJson(API.allPaths + getApiUrl())
        .then(data => {
            createElement('option', SELECTORS.pathsList,
                {'value': 'all', 'text': 'All Paths'});
            data.forEach(option => {
                createElement('option', SELECTORS.pathsList,
                    {'value': option.id, 'text': option.name});
            })
        })
        .then(() => {
            setOptionToSelected(SELECTORS.pathsList, sendData.path.toString());
            putTable();
        })
}

function putTable() {
    let table = SELECTORS.tableElement;
    let row;
    table.textContent = "";
    getJson(API.table + getApiUrl())
        .then(data => {
            data.forEach(elem => {
                row = "<tr><td>" + elem.date + "</td>" +
                    "<td>" + elem.mentor + "</td>" +
                    "<td>" + elem.student + "</td>" +
                    "<td>" + elem.path + "</td></tr>"
                table.innerHTML += row;
            })
        })
}