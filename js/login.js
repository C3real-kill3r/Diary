document.getElementById("LoginForm").addEventListener("submit", function (event) {
  event.preventDefault();
  const username = document.getElementById("username");
  const password = document.getElementById("password");

    credentials = {
        username: username.value,
        password: password.value
    };
    fetch("http://127.0.0.1:5000/api/v2/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(credentials)
        })
        .then((response)=>{
          response.json().then((data) => {
              console.log(data)
        })
        .catch(err => console.log(err));
  })});