pokemon_info = JSON;
collection = "";
//for selectionChanged
SELREQUEST = 1;
SELOFFER = 2;

window.onload = (event) => {
    fetch('/tradegetinfo').then(response => response.json()).then(data => { pokemon_info = data.info; collection = data.collection; initializeRequestSelect(); initializeOfferSelect(); });
};

function initializeRequestSelect() {
    selectRequest = document.getElementById("request");

    for (i = 1; i <= 151; i++) {
        // console.log(typeof i);
        opt = document.createElement("option");

        opt.value = i.toString();

        iPadded = i.toString().padStart(3, '0');
        selection = iPadded + " " + pokemon_info[i].name;
        opt.appendChild(document.createTextNode(selection));

        selectRequest.appendChild(opt);
    }
}

function initializeOfferSelect() {
    selectOffer = document.getElementById("offer");
    collectionInt = [];

    length = collection.length;

    for (var i = 0; i < length; i++) {
        collectionInt.push(parseInt(collection[i]));
    }

    // console.log(collectionInt);
    collectionInt = collectionInt.sort(function (a, b) { return a - b }); // sort only works on strings
    // console.log(collectionInt);
    // console.log(typeof collectionInt[0]);
    for (i = 0; i <= collection.length - 1; i++) {
        opt = document.createElement("option");
        // console.log(typeof collectionInt[0]);
        value = collection[i].toString();
        opt.value = value;

        iPadded = value.padStart(3, '0');
        selection = iPadded + " " + pokemon_info[value].name;
        // selection = " ";
        opt.appendChild(document.createTextNode(selection));

        selectOffer.appendChild(opt);
    }
}
function selectionChanged(sel) {
    if (sel === SELREQUEST) {
        pokeID = document.getElementById("request").value;
        // console.log(pokeID);
        spriteUrl = pokemon_info[pokeID].pokeapiimageurl;
        // console.log(spriteUrl);
        img = document.getElementById("poke1");
        // was super small if I didn't increase sizeborder of image exceeds grid cell, but outer parts of png are empty so doesn't appear to. 
        img.style.width = "70px";
        img.src = spriteUrl;
    } else {
        pokeID = document.getElementById("offer").value;
        // console.log(pokeID);
        spriteUrl = pokemon_info[pokeID].pokeapiimageurl;
        // console.log(spriteUrl);
        img = document.getElementById("poke2");
        // was super small if I didn't increase sizeborder of image exceeds grid cell, but outer parts of png are empty so doesn't appear to. 
        img.style.width = "70px";
        img.src = spriteUrl;
    }
}