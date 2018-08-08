const loginPost = () => {

    fetch('https://diary234.herokuapp.com/api/v2/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          username: document.getElementById('username').value,
          password: document.getElementById('password').value
        }),
        headers: {
          'Content-type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(json => {
        console.log(json)
      })
      .catch(error => {
          console.log(error);
      });
   }