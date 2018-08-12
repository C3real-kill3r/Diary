// fetch for index page
let Message = document.getElementById('welcome');
const WelcomeUrl = 'https://diary234.herokuapp.com/api/v2';

fetch(`${WelcomeUrl}`)
    .then((response)=>{
        response.json().then((data) => {
            console.log(data)
        const welWelcome = Object(data.message)
        const FetchedMessage = `<p class"text_welcome">${welWelcome}</p>`
        Message.innerHTML = FetchedMessage
        })})


        .catch(err => console.log(err));