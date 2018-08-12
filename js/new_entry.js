document.getElementById("entryNew").addEventListener("submit", function (event) {
    event.preventDefault();
    const title = document.getElementById("title");
    const comment = document.getElementById("comment");
    let token = JSON.parse(localStorage.getItem('token'));
  
      credentials = {
          title: title.value,
          comment: comment.value
      };
      fetch("https://diary234.herokuapp.com/api/v2/entries", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json",
                  "x-access-token": token
              },
              body: JSON.stringify(credentials)
          })
          .then((response)=>{
            response.json().then((data) => {
              if (data["message"] == "entry successfully posted!!"){
                window.location.replace("diary_notes.html");
              }
                console.log(data)
                const RegResponse = Object(data.message)
                let Message = document.getElementById("entryPost");
                const FetchedMessage = `<p class"entryMessage">${RegResponse}</p>`
                Message.innerHTML = FetchedMessage
          })
          .catch(err => console.log(err));
    })});