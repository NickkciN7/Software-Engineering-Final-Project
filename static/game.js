GUESS_NUMBER = 0;
CAN_CLICK = true;
NUM_CORRECT = 0;
NUM_INCORRECT = 0;

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

function answerSubmit(buttonNumber) {
    if (!CAN_CLICK) {
        return;
    }
    CAN_CLICK = false;
    // console.log(document.getElementById("choice" + buttonNumber).innerText)
    //GUESS_NUMBER - 1 because number already incremented when updatePage called 
    // console.log(pokemon_info[GUESS_NUMBER - 1].correct.name)
    if (pokemon_info[GUESS_NUMBER - 1].correct.name == document.getElementById("choice" + buttonNumber).innerText) {
        document.getElementById("cORi").innerText = "CORRECT!";
        document.getElementById("cORi").style.color = "Green";
        NUM_CORRECT += 1;
    } else {
        document.getElementById("cORi").innerText = "INCORRECT!";
        document.getElementById("cORi").style.color = "Red";
        NUM_INCORRECT += 1;
    }
    document.getElementById("nextPokemon").style.display = "block";
}

//when next pokemon button is clicked
// at end do something else!!!
function next() {
    document.getElementById("nextPokemon").style.display = "none";
    document.getElementById("gameProg").innerText = GUESS_NUMBER + "/10";
    document.getElementById("numCor").innerText = NUM_CORRECT;
    document.getElementById("numIncor").innerText = NUM_INCORRECT;
    updatePage();
    //allow clicking again
    CAN_CLICK = true;
}