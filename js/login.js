document.getElementById("LoginForm").addEventListener("submit", function (event) {
  event.preventDefault();
  const username = document.getElementById("username");
  const password = document.getElementById("password");

    credentials = {
        username: username.value,
        password: password.value
    };
    fetch("https://diary234.herokuapp.com/api/v2/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(credentials)
        })
        .then((response)=>{
          response.json().then((data) => {
            if (data["message"]["token"]){
              let token = data["message"]["token"]
              localStorage.setItem('token', JSON.stringify(token));
              window.location.replace("diary_notes.html");
            }
            else{
              console.log(data["message"]);
            }
              console.log(data)
              const RegResponse = Object(data.message)
              let Message = document.getElementById("logResponse");
              const FetchedMessage = `<p class"res">${RegResponse}</p>`
              Message.innerHTML = FetchedMessage
        })
        .catch(err => console.log(err));
  })});