async function getAccessToAPI() {
    let token_url = `${window.location.origin}/api/token/`
    let api_url = "http://127.0.0.1:8080/api/"
    let token_response = await fetch(token_url);
    if (token_response.ok) {
        let access_token = await token_response.json();
        let api_response = await fetch(api_url, {
            method: 'GET',
            headers: {
                'Authorization': access_token.access
            }
        })


        console.log(api_response.json())


    }


}



