console.log(document.querySelector('.icon'))
// document.querySelector('.icon').addEventListener("onclick", clicked);
// document.querySelector('.icon').innerHTML = "dupa";

function clicked(arg){
  console.log(arg);
  $.ajax({
    url: "favourites_delete",
    type: "get",
    data: {
      id: arg
    },
    // handle server response if stuff goes well
    success: (data, status) => {
      console.log("dupa");
    },
    // idk what to do if we get to here
    error: (xhr) => {
      alert(xhr)
    }
  });
}

function dupa(){
  console.log("dupa")
}
