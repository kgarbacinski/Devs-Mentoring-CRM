// document.addEventListener('DOMContentLoaded', () => {
//     get_all_meetings()
// })
//
//
//
// function get_all_meetings() {
//     return fetch(get_base_url('/api/meetings/?format=json'))
//         .then(resp => {
//             return resp.json()
//         })
//         .then(data => {
//             console.log(data)
//             // data.forEach(elm => {
//             //     console.log(data)
//             //     // demo.push(elm)
//             // })
//         })
// }
//
//
//
//
// function add_services(category) {
//
//     fetch(get_base_url('/api/meetings/?format=json'))
//         .then(response => {
//             return response.json()
//         })
//         .then(data => {
//             // console.log(data)
//             let meeting = document.getElementById('meeting');
//             let option = document.createElement('ul');
//             meeting.appendChild(option)
//
//             for (let i = 0; i < data.length; i++) {
//                 let li_t = document.createElement('li');
//                 let day = data[i].date.split(',')[0];
//                 let hour = data[i].date.split(',')[1];
//                 let note = data[i].note.text
//                 li_t.innerHTML = `Day: ${day} - Hour: ${hour}   -   Note: ${note}`;
//                 option.appendChild(li_t);
//             }
//
//
//         })
// }
//
// let today = new Date(),
//     currentMonth = today.getMonth(),
//     currentYear = today.getFullYear();
//
// var test;
// get_all_meetings()
// async function get_all_meetings() {
//     const response = await fetch(get_base_url('/api/meetings/?date=' + (currentMonth + 1)));
//     const data = await response.json()
//     test = JSON.parse(JSON.stringify(data))
//     console.log(test)
// }
// console.log(test)


// }
//
// // add_services()