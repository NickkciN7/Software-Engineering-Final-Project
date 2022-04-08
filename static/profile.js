fetch("/profiledata")
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    appendData(data);
  });
function appendData(data) {
  var mainContainer = document.getElementById("myData");
  for (var i = 0; i < data.length; i++) {
    var div = document.createElement("div");
    var img = new Image();
    img.src = data[i].imageurl;
    div.innerHTML = "Name: " + data[i].name;
    mainContainer.appendChild(div);
    mainContainer.appendChild(img);
  }
}
