document.addEventListener('DOMContentLoaded', function () {
    showYear()
    displayAllMeetings()
}, false);


function showNoteText(id_obj, element) {
    getJson('/api/notes/?id=' + id_obj)
        .then(data => {
            if (data.length > 0) {
                element.innerHTML =  data[0].text
            }
        })
}