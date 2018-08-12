document.getElementById("Register").addEventListener("submit", function (event) {
  event.preventDefault();
  const fname = document.getElementById("fname");
  const lname = document.getElementById("lname");
  const username = document.getElementById("username");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const con_password = document.getElementById("con_password");

    credentials = {
        fname: fname.value,
        lname: lname.value,
        username: username.value,
        email: email.value,
        password: password.value,
        con_password: con_password.value
    };
    fetch("https://diary234.herokuapp.com/api/v2/auth/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept":"application/json"
            },
            body: JSON.stringify(credentials)
        })
        .then((response)=>{
          response.json().then((data) => {
            if (data["message"] == "you are succesfully registered"){
                window.location.replace("login.html");
            }
            console.log(data)
            const RegResponse = Object(data.message)
            let Message = document.getElementById("regResponse");
            const FetchedMessage = `<p class"res">${RegResponse}</p>`
            Message.innerHTML = FetchedMessage  
        })
        .catch(err => console.log(err));
  })});