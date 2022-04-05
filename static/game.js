GUESS_NUMBER = 0;

pokemon_info = JSON;

window.onload = (event) => {
    // fetch('/gamedata').then(response => response.json()).then(data => pokemon_info = data);

    fetch('/gamedata').then(response => response.json()).then(data => { pokemon_info = data; updatePage(); console.log(data); });

};

function updatePage() {
    image = document.getElementById("image");
    // set the image to the current pokemon to guess
    image.src = pokemon_info[GUESS_NUMBER].correct.imageurl;
    // a list of the pokemon names
    pokeNames = [];
    // push the correct pokemon name
    pokeNames.push(pokemon_info[GUESS_NUMBER].correct.name);
    // add the incorrect names
    pokeNames = pokeNames.concat(pokemon_info[GUESS_NUMBER].incorrect);
    // randomly assign pokemon names to 1 of the 4 buttons
    buttonAssignment = [];
    for (var i = 1; i <= 4; i++) {
        currentIndex = Math.floor(Math.random() * pokeNames.length);
        buttonAssignment.push(pokeNames[currentIndex]);
        pokeNames.splice(currentIndex, 1);
    }

    button1 = document.getElementById("choice1");
    button2 = document.getElementById("choice2");
    button3 = document.getElementById("choice3");
    button4 = document.getElementById("choice4");

    // set the buttons' text to pokemon names
    button1.innerText = buttonAssignment[0];
    button2.innerText = buttonAssignment[1];
    button3.innerText = buttonAssignment[2];
    button4.innerText = buttonAssignment[3];

    GUESS_NUMBER += 1;
}