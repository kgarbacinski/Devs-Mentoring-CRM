// carousel splide js:
new Splide('.splide', {
    type: 'loop',
    perMove: 1,
    perPage: 5,
    breakpoints: {
        1450: {
            perPage: 4,
        },
        1200: {
            perPage: 3,
        },
        850: {
            perPage: 2,
        },
        560: {
            perPage: 1,
        }
    }
}).mount();

// sprawdzenie czy lepiej mozna szukac
// pupup on mobile:
const themeName = document.querySelectorAll('a.theme-name.available')
const themeDetails = document.querySelector('.themes-details')
const backBtn = document.querySelector('.back-btn')
// #klasa seleketor pola statyczxne
let fileDetails = themeDetails.children
let tittle = fileDetails.namedItem('tittle')
let description = fileDetails.namedItem('description')
let filesContainer = fileDetails.namedItem('container')
let filesList = filesContainer.children.namedItem('filesListContainer').children.namedItem('filesList')
let AccessUsersListForOneSubTopic = document.getElementsByClassName("shared-for-student-list")[0].children.namedItem("shared_for_one")
let NotAccessUsersListForOneSubTopic = document.getElementsByClassName("sharing-student-list")[0].children.namedItem("share_for_one")
let ThemeNameForOne = document.getElementsByClassName("theme-name").namedItem('tittle_modal_for_one')
let ThemeNameForSubject = document.getElementsByClassName("category-name").namedItem("tittle_modal_for_subject")
let AccessUsersListForSubject = document.getElementsByClassName("shared-for-student-list")[1].children.namedItem("shared_for_all")
let NotAccessUsersListForSubject = document.getElementsByClassName("sharing-student-list")[1].children.namedItem("share_for_all")
let curr_subtopic = ""
let curr_subject =""

console.log(ThemeNameForSubject)
console.log(ThemeNameForOne)


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


const showDetails = () => {
    if (themeDetails.style.display = "none") {
        themeDetails.style.display = "block"
    }
}

const closeDetails = () => {
    if (themeDetails.style.display = "block") {
        themeDetails.style.display = "none"
    }
}

const themeNames = themeName.forEach(name => name.addEventListener('click', showDetails))
backBtn.addEventListener('click', closeDetails)


// js for search engines in modals:

// 1- shared for:
const searchShared = document.querySelector('.search-shared-for')
const liShared = document.querySelectorAll('.shared-for-student-name')

const searchEngine = (e) => {
    const text = e.target.value.toLowerCase();
    liShared.forEach(el => {

        if (el.textContent.toLowerCase().indexOf(text) !== -1) {
            el.style.display = 'block'
        } else {
            el.style.display = 'none'
        }
    })
}

searchShared.addEventListener('keyup', searchEngine)

// 2- sharing:
const searchSharing = document.querySelector('.search-sharing')
const liSharing = document.querySelectorAll('.sharing-student-name')

const searchEngine2 = (e) => {
    const text = e.target.value.toLowerCase();
    liSharing.forEach(el => {

        if (el.textContent.toLowerCase().indexOf(text) !== -1) {
            el.style.display = 'block'
        } else {
            el.style.display = 'none'
        }
    })
}

searchSharing.addEventListener('keyup', searchEngine2)


async function getFiles(subtopic_id) {
    url = (window.location.origin + '/api/files/' + subtopic_id)
    console.log(url)
    let response = await fetch(url);
    let files = await response.json();
    console.log(files)
    filesList.innerHTML = '';
    themeDetails.style.visibility = 'visible';
    tittle.innerHTML = files[0].subtopic_name;
    description.innerHTML = files[0].subtopic_description;

    files.forEach(obj => {
        Object.entries(obj).forEach(([key, value]) => {
            file_url = obj.docfile
            file_name = obj.name

        });
        let a = document.createElement('a');
        a.href = file_url
        a.innerHTML = "<i class=\"bi bi-file-earmark-arrow-down\"></i><span\n" +
            "class=\"file-name\">" + file_name + "</span>"

        filesList.appendChild(a)

        console.log(file_url)
        console.log(file_name)
    });

}

async function getUsersOneSubTopic(subtopic_id) {

    url = (window.location.origin + '/api/access/files/' + subtopic_id)
    console.log(url)
    let response = await fetch(url);
    let users = await response.json();
    curr_subtopic = subtopic_id
    AccessUsersListForOneSubTopic.innerHTML = ''
    NotAccessUsersListForOneSubTopic.innerHTML = ''
    ThemeNameForOne.innerHTML = users[0].subtopic_name

    users.forEach(obj => {
        Object.entries(obj).forEach(([key, value]) => {
            user_id = obj.id
            user_first_name = obj.first_name
            user_last_name = obj.last_name
            access = obj.access


        });

        let li = document.createElement('li');
        let p = document.createElement('p');
        let button = document.createElement("button");
        let i = document.createElement('i')
        p.className = 'student-name'
        button.className = "student-delete"
        p.innerHTML = user_first_name + " " + user_last_name

        if (access) {
            i.className = "bi bi-dash-lg"
            button.addEventListener("click", deleteUserToOneSubTopic.bind(null, user_id, subtopic_id));
            button.appendChild(i)
            p.appendChild(button)
            li.appendChild(p)
            AccessUsersListForOneSubTopic.appendChild(li)

        } else {

            i.className = "bi bi-plus-lg"
            button.addEventListener("click", addUserToOneSubTopic.bind(null, user_id, subtopic_id));
            button.appendChild(i)
            p.appendChild(button)
            li.appendChild(p)
            NotAccessUsersListForOneSubTopic.appendChild(li)

        }

    });


}

async function addUserToOneSubTopic(user_id, subtopic_id) {
    url = (window.location.origin + '/api/access/files/' + subtopic_id + "/")
    const config = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken

        },
        body: JSON.stringify(user_id),
    }
    const response = await fetch(url, config)
    if (response.ok) {
        await getUsersOneSubTopic(subtopic_id)

    }
}

async function deleteUserToOneSubTopic(user_id, subtopic_id) {
    url = (window.location.origin + '/api/access/files/' + subtopic_id + "/")
    const config = {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken

        },
        body: JSON.stringify(user_id),
    }
    const response = await fetch(url, config)
    if (response.ok) {
        await getUsersOneSubTopic(subtopic_id)
    }
}


async function getUsersSubject(subject_id) {
    url = (window.location.origin + '/api/access/subject/' + subject_id)
    console.log(url)
    curr_subject = subject_id
    let response = await fetch(url);
    let users = await response.json();
    AccessUsersListForSubject.innerHTML = ''
    NotAccessUsersListForSubject.innerHTML = ''
    ThemeNameForSubject.innerHTML = users[0].subject_name

    users.forEach(obj => {
        Object.entries(obj).forEach(([key, value]) => {
            user_id = obj.id
            user_first_name = obj.first_name
            user_last_name = obj.last_name
            access = obj.access


        });

        let li = document.createElement('li');
        let p = document.createElement('p');
        let button = document.createElement("button");
        let i = document.createElement('i')
        p.className = 'student-name'
        button.className = "student-delete"
        p.innerHTML = user_first_name + " " + user_last_name
        if (access) {
            i.className = "bi bi-dash-lg"
            button.addEventListener("click", deleteUserToSubject.bind(null, user_id, subject_id));
            button.appendChild(i)
            p.appendChild(button)
            li.appendChild(p)
            AccessUsersListForSubject.appendChild(li)

        } else {

            i.className = "bi bi-plus-lg"
            button.addEventListener("click", addUserToSubject.bind(null, user_id, subject_id));
            button.appendChild(i)
            p.appendChild(button)
            li.appendChild(p)
            NotAccessUsersListForSubject.appendChild(li)

        }

    });


}


async function addUserToSubject(user_id, subject_id) {
    let url = (window.location.origin + '/api/access/subject/' + subject_id + "/")
    const config = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken

        },
        body: JSON.stringify(user_id),
    }
    const response = await fetch(url, config)
    if (response.ok) {
        await getUsersSubject(subject_id)

    }
}


async function deleteUserToSubject(user_id, subject_id) {
    let url = (window.location.origin + '/api/access/subject/' + subject_id + "/")
    const config = {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken

        },
        body: JSON.stringify(user_id),
    }
    const response = await fetch(url, config)
    if (response.ok) {
        await getUsersSubject(subject_id)
    }
}

async function getSharedUsersSearchboxSubtopic() {
    let text = document.getElementById('search-shared-for-subtopic').value
    if (text) {


        let url = (window.location.origin + '/api/access/searchbox/subtopic/' + curr_subtopic + "/" + "?text=" + text + "&access=1"
        )
        let response = await fetch(url);
        if (response.ok) {
            let users = await response.json();
            AccessUsersListForOneSubTopic.innerHTML = ''

            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                });

                let li = document.createElement('li');

                let p = document.createElement('p');
                let button = document.createElement("button");
                let i = document.createElement('i')
                p.className = 'student-name'
                button.className = "student-delete"
                p.innerHTML = user_first_name + " " + user_last_name

                i.className = "bi bi-dash-lg"
                button.addEventListener("click", deleteUserToOneSubTopic.bind(null, user_id, curr_subtopic));
                button.appendChild(i)
                p.appendChild(button)
                li.appendChild(p)
                AccessUsersListForOneSubTopic.appendChild(li)
            })


        }

    } else {

        await getUsersOneSubTopic(curr_subtopic)


    }
}


async function GetNotSharedUsersSearchBoxSubtopic() {
    let text = document.getElementById('search-sharing-subtopic').value
    if (text) {


        let url = (window.location.origin + '/api/access/searchbox/subtopic/' + curr_subtopic + "/" + "?text=" + text + "&access=0"
        )
        let response = await fetch(url);
        if (response.ok) {
            let users = await response.json();
            NotAccessUsersListForOneSubTopic.innerHTML = ''

            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                });

                let li = document.createElement('li');

                let p = document.createElement('p');
                let button = document.createElement("button");
                let i = document.createElement('i')
                p.className = 'student-name'
                button.className = "student-delete"
                p.innerHTML = user_first_name + " " + user_last_name

                i.className = "bi bi-plus-lg"
                button.addEventListener("click", addUserToOneSubTopic.bind(null, user_id, curr_subtopic));
                button.appendChild(i)
                p.appendChild(button)
                li.appendChild(p)
                NotAccessUsersListForOneSubTopic.appendChild(li)
            })


        }

    } else {

        await getUsersOneSubTopic(curr_subtopic)


    }
}

async function getSharedUsersSearchboxSubject() {
    console.log(curr_subject)
    let text = document.getElementById('search-shared-for-subject').value
    console.log(text)
    if (text) {


        let url = (window.location.origin + '/api/access/searchbox/subject/' + curr_subject + "/" + "?text=" + text + "&access=1"
        )
        let response = await fetch(url);
        if (response.ok) {
            let users = await response.json();
            AccessUsersListForSubject.innerHTML = ''
            console.log(users)

            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                });

                let li = document.createElement('li');

                let p = document.createElement('p');
                let button = document.createElement("button");
                let i = document.createElement('i')
                p.className = 'student-name'
                button.className = "student-delete"
                p.innerHTML = user_first_name + " " + user_last_name

                i.className = "bi bi-dash-lg"
                button.addEventListener("click", deleteUserToSubject.bind(null, user_id, curr_subject));
                button.appendChild(i)
                p.appendChild(button)
                li.appendChild(p)
                AccessUsersListForSubject.appendChild(li)
            })


        }

    } else {

        await getUsersSubject(curr_subject)


    }
}

async function getNotSharedUsersSearchboxSubject() {
    console.log(curr_subject)
    let text = document.getElementById('search-sharing-for-subject').value
    console.log(text)
    if (text) {


        let url = (window.location.origin + '/api/access/searchbox/subject/' + curr_subject + "/" + "?text=" + text + "&access=0"
        )
        let response = await fetch(url);
        if (response.ok) {
            let users = await response.json();
            NotAccessUsersListForSubject.innerHTML = ''
            console.log(users)

            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                });

                let li = document.createElement('li');

                let p = document.createElement('p');
                let button = document.createElement("button");
                let i = document.createElement('i')
                p.className = 'student-name'
                button.className = "student-delete"
                p.innerHTML = user_first_name + " " + user_last_name

                i.className = "bi bi-plus-lg"
                button.addEventListener("click", addUserToSubject.bind(null, user_id, curr_subject));
                button.appendChild(i)
                p.appendChild(button)
                li.appendChild(p)
                NotAccessUsersListForSubject.appendChild(li)
            })


        }

    } else {

        await getUsersSubject(curr_subject)


    }
}