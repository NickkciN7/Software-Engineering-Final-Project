GUESS_NUMBER = 0;
CAN_CLICK = true;
NUM_CORRECT = 0;
NUM_INCORRECT = 0;
PROFILE_POINTS = 0;

pokemon_info = JSON;

window.onload = (event) => {
    // fetch('/gamedata').then(response => response.json()).then(data => pokemon_info = data);

    fetch('/gamedata').then(response => response.json()).then(data => { pokemon_info = data; updatePage(); initializeImages(); console.log(data); });
    fetch('/gamegetpoints').then(response => response.json()).then(data => { PROFILE_POINTS = data.points; });
};


// load all images in different img tags because loading each turn causes lag ~2-3 seconds
function initializeImages() {
    for (i = 1; i <= 10; i++) {
        image = document.getElementById("image" + i);
        // set the image to the current pokemon to guess
        image.src = pokemon_info[i - 1].correct.imageurl;
    }
}

function updatePage() {
    curr_id = "image" + (GUESS_NUMBER + 1).toString();

    document.getElementById(curr_id).style.display = "inline-block";
    // set the image to the current pokemon to guess
    if (GUESS_NUMBER != 0) {
        prev_id = "image" + (GUESS_NUMBER).toString();
        document.getElementById(prev_id).style.display = "none";
    }

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

    //GUESS_NUMBER - 1 because number already incremented when updatePage called 

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
    if (GUESS_NUMBER == 10) {
        document.getElementById("nextPokeButton").style.display = "none";
        document.getElementById("resultsButton").style.display = "inline-block";
    }

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

//display results
function finish() {
    document.getElementById("game").style.display = "none";
    document.getElementById("finish").style.display = "block";
    document.getElementById("cor").innerText = NUM_CORRECT;
    document.getElementById("cor2").innerText = NUM_CORRECT;
    document.getElementById("incor").innerText = NUM_INCORRECT;
    document.getElementById("updatedpoints").innerText = (PROFILE_POINTS + NUM_CORRECT);

    const dataToSend = { points: NUM_CORRECT };
    fetch('/gameupdatepoints', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
    }).then(response => response.json()).then(data => {
        console.log('Success:', data);
    });
}