let token = JSON.parse(localStorage.getItem('token'));
fetch("https://diary234.herokuapp.com/api/v2/entries", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept":"application/json",
                "x-access-token":token
            },
           // body: JSON.stringify(credentials)
        })
        .then((response)=>{
          response.json().then((data) => {
            if (data["message"] == "Token is missing!" || data["message"] == "Token is invalid!"){
                window.location.replace("login.html");
            }
            else{
                let diaryPosts =`<div id="resTable">
                <ul class="responsive-table" id="table">
                <li class="table-header">
                  <div class="col col-1">Id</div>
                  <div class="col col-2">title</div>
                  <div class="col col-3">date</div>
                  <div class="col col-4"></div>
                  <div class="col col-5"></div>
                  <div class="col col-6"></div>
                </li>`;
                Object.keys(data).forEach(function(entr){
                  diaryPosts +=`<li class="table-row">
                    <div class="col col-1" id="commentId">${data[entr]["entry_id"]}</div>
                      <div class="col col-2" id="title">${data[entr]["title"]}</div>
                    <div class="col col-3" id="date">${data[entr]["time"]}</div>
                    <div class="col col-6"><input type="submit" id="myBtn" value="view"></div>
                    <div class="col col-4"><input type="submit" id="edit" value="edit"></div>
                    <div class="col col-5"><input type="submit" id="delete" value="delete"></div>
                  </li>`;
                });
                document.getElementById("tform").innerHTML = diaryPosts + `</ul></div>`;
            }
              console.log(data)
          })
        .catch(err => console.log(err));
  })
const logout = () => {
    localStorage.clear();
  }