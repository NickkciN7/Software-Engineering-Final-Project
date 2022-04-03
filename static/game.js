pokemon_info = {};

window.onload = (event) => {
    // fetch('/gamedata').then(response => response.json()).then(data => pokemon_info = data);

    fetch('/gamedata').then(response => response.json()).then(data => console.log(JSON.stringify(data)));

};