fetch("/profiledata")
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    appendData(data);
  });
function appendData(data) {
  var mainContainer = document.getElementById("myData");
  var i = 0;
  var div = null;
  var image = null;
  for (i = 0; i < data.length; i++) {
    div = document.createElement("div");
    img = new Image();
    img.src = data[i].imageurl;
    div.innerHTML = "Name: " + data[i].name;
    mainContainer.appendChild(div);
    mainContainer.appendChild(img);
  }
}
