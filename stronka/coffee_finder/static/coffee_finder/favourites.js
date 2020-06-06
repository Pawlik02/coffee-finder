document.querySelector('.icon').addEventListener("onclick", click);
document.querySelector('.icon').innerHTML = "dupa";

function click(){
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
      alert("Dupa");
    },
    // idk what to do if we get to here
    error: (xhr) => {
      alert("cant have shit in ajax")
    }
  });
}
console.log(document.querySelector('.icon'))
