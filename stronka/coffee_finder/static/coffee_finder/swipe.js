document.querySelector('#left').addEventListener("mouseover", mouseOverLeft);
document.querySelector('.content').addEventListener("mouseout", mouseOut);
document.querySelector('#left').addEventListener("onclick", mouseClickLeft);
document.querySelector('#right').addEventListener("mouseover", mouseOverRight);
document.querySelector('#right').addEventListener("onclick", mouseClickRight);

function mouseOverLeft() {
  document.querySelector('.content').style.transform = "rotate(-10deg)";
}
function mouseOut(){
  document.querySelector('.content').style.transform = "rotate(0deg)";
  document.querySelector('.content').classList.remove("clickedR");
  document.querySelector('.content').classList.remove("clickedL");
}

function mouseOverRight() {
  document.querySelector('.content').style.transform = "rotate(10deg)";
}

// function mouseOutRight() {
//   document.querySelector('.content').style.transform = "rotate(0deg)";
// }

function mouseClickRight() {
  document.querySelector('.content').classList.add("clickedR");
}

function mouseClickLeft(){
  document.querySelector('.content').classList.add("clickedL");
}
