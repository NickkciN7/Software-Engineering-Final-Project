var head = document.getElementsByTagName('HEAD')[0];
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = 'style.css';
head.appendChild(link);

fetch("/ranking", {
    method: "POST",
}).then(res => res.json())
    .then(data => listSorted(data.user_list));

function listSorted(data) {
    var display_list = document.getElementById("display_list");
    var listView = document.createElement('ol');
    listView.className = "list";
    for (var i = 0; i < data.length; i++) {
        var listItem = document.createElement('li');
        var userList = document.createElement('a')
        userList.textContent = data[i].username;
        userList.href = "/user_profile/" + data[i].id
        var userPoints = document.createTextNode(data[i].lifetimepoints);
        // userPoints.className = "right";
        var div = document.createElement("div");
        div.appendChild(userList);
        div.appendChild(userPoints);
        listItem.appendChild(div);
        // listItem.appendChild(userList);
        listView.appendChild(listItem);
    }
    display_list.appendChild(listView);
}

function sortAsc() {
    var listItem = document.getElementById("display_list")
    listItem.innerHTML = ""
    fetch("/ranking", {
        method: "POST",
    }).then(res => res.json())
        .then(data => listSorted(data.user_list));
}

function sortDesc() {
    var listItem = document.getElementById("display_list")
    listItem.innerHTML = ""
    fetch("/ranking", {
        method: "POST",
    }).then(res => res.json())
        .then(data => listSorted(data.user_list.reverse()));
}

