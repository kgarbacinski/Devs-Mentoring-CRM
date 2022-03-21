let Selectors = { "code_field" : document.getElementById("code-form").elements['code'],
                    "info_header" : document.getElementById('info')

}

document.getElementById('send-button').addEventListener('click',  function(){
     sendToComputing()
         .then(() => {console.log()})
     saveCodeToDB();
})


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

async function saveCodeToDB(){
    let data = {}
    data.code = Selectors['code_field'].value
    let url = `${window.location.origin}/api/access/exercises/code/${exercise_status_id}`
    let config = {
            method: 'PATCH',
            headers: {
            'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie("csrftoken")
            },
            body: JSON.stringify(data)
        }
    let response = await fetch(url, config)
    console.log(response)
}

async function getToken(){
    let token_url = `${window.location.origin}/api/token/`
    let token_response = await (await fetch(token_url)).json();
    return token_response.access
}

async function sendToComputing() {
    let data = {}
    let computing_url = "http://127.0.0.1:8002/"
    let token = await getToken()
    data.code = Selectors['code_field'].value
    data.language = language
    data.name = slug_name
    console.log(data)
    console.log(data.code)
    let config = {
        method: 'POST',
        headers: {
        'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token,
            'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify(data)
    }
    
    let computing_response = await fetch(computing_url, config)
    let body = await computing_response.json()

    if (computing_response.ok){

        if(body.done === true){
            window.alert("OK!")

        }
        else if (body.done=== false){
            window.alert(`TEST PASSED:${body.test_passed}`)

        }
            
        }

    else{
            Selectors["info_header"].innerText = body.error

    }

        }



    






