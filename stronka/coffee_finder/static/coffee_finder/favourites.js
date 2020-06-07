console.log(document.querySelector('.icon'))
document.querySelector('.icon').addEventListener("onclick", clicked);
// document.querySelector('.icon').innerHTML = "dupa";

function clicked(){
  console.log("string");
  $.ajax({
    url: "favourites_delete",
    type: "get",
    // specify swipe direcion
    data: {
      name: "dupa"
    },
    // handle server response if stuff goes well
    success: (data, status) => {
      alert("dupa");
    },
    // idk what to do if we get to here
    error: (xhr) => {
      alert("cant have shit in ajax")
    }
  });
}

function dupa(){
  console.log("dupa")
}
